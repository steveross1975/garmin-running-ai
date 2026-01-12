"""Process Garmin splits CSV (per-km aggregated running dynamics)."""
from pathlib import Path

import pandas as pd
from config import DATA_DIR, is_pipeline_mode

SPLITS_DIR = DATA_DIR / "splits"
SPLITS_DIR.mkdir(exist_ok=True)


def load_splits_csv(splits_path: Path) -> pd.DataFrame:
    """Load and clean splits CSV."""
    print(f"📊 Loading splits: {splits_path.name}")
    
    df = pd.read_csv(splits_path)
    
    print(f"   Columns: {list(df.columns)}")
    print(f"   Rows (km): {len(df)}")
    print(f"   Metrics: {df.dtypes.to_dict()}")
    
    return df


def analyze_splits(df: pd.DataFrame, activity_id: str) -> dict:
    """Analyze per-km metrics from splits CSV."""
    analysis = {
        "activity_id": activity_id,
        "total_km": len(df),
        "avg_pace_min_km": df["pace"].mean() if "pace" in df else None,
        "avg_cadence": df["cadence"].mean() if "cadence" in df else None,
        "avg_heart_rate": df["heart_rate"].mean() if "heart_rate" in df else None,
        "avg_vertical_osc": df["vertical_oscillation"].mean() if "vertical_oscillation" in df else None,
        "avg_gct": df["gct"].mean() if "gct" in df else None,
        "avg_gct_balance": df["gct_balance"].mean() if "gct_balance" in df else None,
        "avg_step_speed_loss": df["step_speed_loss"].mean() if "step_speed_loss" in df else None,
        "cadence_trend": "increasing" if df["cadence"].iloc[-1] > df["cadence"].iloc[0] else "decreasing",
        "hr_trend": "increasing" if df["heart_rate"].iloc[-1] > df["heart_rate"].iloc[0] else "decreasing",
    }
    
    return analysis


if __name__ == "__main__":
    """Test splits processor."""
    if is_pipeline_mode():
        print("🚫 Use pipeline.py instead")
    exit(1)
    print("🚀 Garmin Splits CSV Processor")
    print("=" * 50)
    
    # Find splits CSVs
    splits_files = list(SPLITS_DIR.glob("*.csv"))
    
    if not splits_files:
        print(f"❌ No splits CSV found in {SPLITS_DIR}")
        print("📋 Copy your Garmin splits CSV files there first:")
        print("   Garmin Connect → Activity → Export → splits.csv → copy to data/splits/")
        exit(1)
    
    print(f"📁 Found {len(splits_files)} splits files\n")
    
    for splits_file in splits_files:
        df = load_splits_csv(splits_file)
        analysis = analyze_splits(df, splits_file.stem)
        
        print(f"\n📊 ANALYSIS: {splits_file.stem}")
        print(f"   Distance: {analysis['total_km']} km")
        print(f"   Avg Cadence: {analysis['avg_cadence']:.1f} spm")
        print(f"   Avg HR: {analysis['avg_heart_rate']:.0f} bpm")
        print(f"   Avg Vertical Osc: {analysis['avg_vertical_osc']:.2f} cm" if analysis['avg_vertical_osc'] else "   VO: N/A")
        print(f"   Avg GCT: {analysis['avg_gct']:.0f} ms" if analysis['avg_gct'] else "   GCT: N/A")
        print(f"   Avg Step Speed Loss: {analysis['avg_step_speed_loss']:.2f} cm/s" if analysis['avg_step_speed_loss'] else "   SSL: N/A")
        print(f"   Cadence trend: {analysis['cadence_trend']}")
        print(f"   HR trend: {analysis['hr_trend']}")
