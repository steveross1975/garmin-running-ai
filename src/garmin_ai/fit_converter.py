"""FIT to CSV converter - Extracts all Garmin running dynamics."""
import csv
from pathlib import Path
from typing import Any, Dict, List

import fitparse
import pandas as pd

from .config import CSV_DIR

RUNNING_DYNAMICS_FIELDS = [
    "timestamp",
    "position_lat", "position_long", "altitude",
    "distance", "speed", "cadence", "heart_rate",
    "vertical_oscillation", "vertical_ratio",
    "ground_time", "stance_time", "stance_time_balance",
    "stepspeedloss", "stepSpeedLossPercent", "fractional_cadence",
    "grade_adjusted_speed", "grade", "power",
    "left_torso_angle", "right_torso_angle",
    "left_pelvis_angle", "right_pelvis_angle",
    "left_leg_angle", "right_leg_angle",
]


def fit_to_csv(fit_path: Path, csv_path: Path) -> Dict[str, Any]:
    """Convert FIT to CSV + compute summary stats."""
    print(f"🔄 Converting {fit_path.name}...")
    
    fitfile = fitparse.FitFile(
        str(fit_path),
        data_processor=fitparse.StandardUnitsDataProcessor()
    )
    
    records = []
    for record in fitfile.get_messages("record"):
        row = {}
        for field in record:
            if field.name in RUNNING_DYNAMICS_FIELDS:
                row[field.name] = field.value
        if "timestamp" in row:
            records.append(row)
    
    if not records:
        raise ValueError(f"No record data in {fit_path}")
    
    # Write CSV
    with open(csv_path, "w", newline="", encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=RUNNING_DYNAMICS_FIELDS)
        writer.writeheader()
        writer.writerows(records)
    
    # Summary stats with pandas
    df = pd.DataFrame(records)
    summary = {
        "file": fit_path.name,
        "records": len(df),
        "duration_min": (df["timestamp"].max() - df["timestamp"].min()).total_seconds() / 60,
        "distance_km": df["distance"].max() / 1000 if "distance" in df else 0,
        "avg_speed_kmh": df["speed"].mean() * 3.6 if "speed" in df else 0,
        "avg_cadence": df["cadence"].mean() if "cadence" in df else 0,
        "avg_hr": df["heart_rate"].mean() if "heart_rate" in df else 0,
        "has_vertical_osc": "vertical_oscillation" in df.columns,
        "has_gct": "ground_time" in df or "stance_time" in df,
        "has_step_loss": "stepspeedloss" in df.columns,
    }
    
    return summary


def convert_recent_fit_files(n_recent: int = 3) -> List[Dict[str, Any]]:
    """Convert N most recent FIT files to CSV."""
    from .garmin_client import get_recent_fit_files
    
    fit_files = get_recent_fit_files(n_recent)
    if not fit_files:
        return []
    
    summaries = []
    for fit_file in fit_files:
        csv_file = CSV_DIR / f"{fit_file.stem}.csv"
        
        if csv_file.exists():
            print(f"⏭️  {csv_file.name} already exists")
            continue
        
        try:
            summary = fit_to_csv(fit_file, csv_file)
            summaries.append(summary)
            print(f"✅ {summary['file']} → {summary['records']} records, {summary['duration_min']:.1f}min")
        except Exception as e:
            print(f"❌ {fit_file.name}: {e}")
    
    return summaries


# if __name__ == "__main__":
#     """Test converter."""
#     print("🚀 FIT → CSV Converter")
#     print("=" * 50)
#     summaries = convert_recent_fit_files(n_recent=3)
    
#     print("\n📊 SUMMARY:")
#     for s in summaries:
#         print(f"  {s['file']}: {s['records']} records, "
#               f"{s['duration_min']:.1f}min, "
#               f"{s['avg_cadence']:.0f}spm, "
#               f"{s['avg_hr']:.0f}bpm")

if __name__ == "__main__":
    """Test converter with DEBUG output."""
    print("🚀 FIT → CSV Converter - DEBUG MODE")
    print("=" * 50)
    
    # DEBUG 1: Check garmin_client works
    from .garmin_client import get_recent_fit_files
    print("\n🔍 STEP 1: Finding FIT files...")
    fit_files = get_recent_fit_files(n_recent=3)
    print(f"   Found {len(fit_files)} FIT files")
    
    if not fit_files:
        print("❌ No FIT files - check data/fit/")
        exit(1)
    
    # DEBUG 2: Test first file manually
    print(f"\n🔍 STEP 2: Testing first file: {fit_files[0].name}")
    csv_file = CSV_DIR / f"{fit_files[0].stem}.csv"
    print(f"   Output: {csv_file}")
    
    if csv_file.exists():
        print(f"⏭️  CSV already exists: {csv_file}")
    else:
        print("   Converting...")
        try:
            summary = fit_to_csv(fit_files[0], csv_file)
            print(f"✅ SUCCESS: {summary}")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            import traceback
            traceback.print_exc()