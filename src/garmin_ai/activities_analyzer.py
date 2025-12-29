"""Analyze Garmin Activities.csv - comprehensive running metrics."""
from pathlib import Path

import numpy as np
import pandas as pd

from .config import DATA_DIR

ACTIVITIES_CSV = DATA_DIR / "Activities.csv"


def load_activities(csv_path: Path = ACTIVITIES_CSV) -> pd.DataFrame:
    """Load Garmin Activities.csv with all running metrics."""
    if not csv_path.exists():
        print(f"❌ {csv_path} not found")
        return pd.DataFrame()
    
    print(f"📊 Loading: {csv_path.name}")
    df = pd.read_csv(csv_path)
    
    print(f"   ✅ Loaded {len(df)} activities")
    print(f"   Columns ({len(df.columns)}): {list(df.columns)}")
    
    return df


def parse_time_to_seconds(time_str: str) -> float:
    """Convert HH:MM:SS to seconds."""
    try:
        parts = str(time_str).split(':')
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return 0
    except Exception:
        return 0


def parse_gct_balance(balance_str: str) -> tuple:
    """Parse GCT Balance like '50.1% L / 49.9% R' to (left%, right%)."""
    try:
        parts = str(balance_str).replace('%', '').split('/')
        left = float(parts[0].strip().replace('L', ''))
        right = float(parts[1].strip().replace('R', ''))
        return (left, right)
    except Exception:
        return (50, 50)


def analyze_activities(df: pd.DataFrame) -> dict:
    """Comprehensive analysis of all running activities."""
    if df.empty:
        return {}
    
    # Clean data
    df_clean = df.copy()
    
    # Parse times to seconds
    df_clean['Time_Seconds'] = df['Time'].apply(parse_time_to_seconds)
    df_clean['Moving_Time_Seconds'] = df['Moving Time'].apply(parse_time_to_seconds)
    
    # Parse GCT Balance
    df_clean[['GCT_Balance_Left', 'GCT_Balance_Right']] = df['Avg GCT Balance'].apply(
        lambda x: pd.Series(parse_gct_balance(x))
    )
    
    analysis = {
        "num_activities": len(df),
        "total_distance_km": df['Distance'].sum(),
        "total_time_hours": df_clean['Time_Seconds'].sum() / 3600,
        
        # Running Cadence
        "avg_cadence": df['Avg Run Cadence'].mean(),
        "max_cadence": df['Max Run Cadence'].max(),
        "min_cadence": df['Avg Run Cadence'].min(),
        "cadence_range": df['Max Run Cadence'].max() - df['Avg Run Cadence'].min(),
        
        # Heart Rate
        "avg_hr": df['Avg HR'].mean(),
        "max_hr": df['Max HR'].max(),
        "min_hr": df['Avg HR'].min(),
        "hr_zone_efficiency": df['Avg HR'].mean() / df['Max HR'].max() * 100,  # % of max
        
        # Running Dynamics
        "avg_vertical_oscillation": df['Avg Vertical Oscillation'].mean(),
        "avg_vertical_ratio": df['Avg Vertical Ratio'].mean(),
        "avg_ground_contact_time": df['Avg Ground Contact Time'].mean(),
        "avg_step_speed_loss_cms": df['Avg Step Speed Loss'].mean(),
        "avg_step_speed_loss_pct": df['Avg Step Speed Loss %'].mean(),
        "avg_stride_length": df['Avg Stride Length'].mean(),
        
        # GCT Balance (left/right)
        "avg_gct_balance_left": df_clean['GCT_Balance_Left'].mean(),
        "avg_gct_balance_right": df_clean['GCT_Balance_Right'].mean(),
        
        # Pace & Power
        "avg_pace_min_km": df['Avg Pace'].astype(str).str.split(':').apply(
            lambda x: int(x[0]) * 60 + int(x[1]) if len(x) == 2 else 0
        ).mean() / 60,
        "avg_power": df['Avg Power'].mean(),
        
        # Training Metrics
        "total_aerobic_te": df['Aerobic TE'].sum(),
        "avg_aerobic_te": df['Aerobic TE'].mean(),
        "total_calories": df['Calories'].sum(),
        
        # Activity Details
        "activities": []
    }
    
    # Per-activity details
    for idx, row in df.iterrows():
        activity = {
            "date": row['Date'],
            "distance": row['Distance'],
            "time": row['Time'],
            "avg_hr": row['Avg HR'],
            "cadence": row['Avg Run Cadence'],
            "vertical_osc": row['Avg Vertical Oscillation'],
            "gct": row['Avg Ground Contact Time'],
            "step_loss": row['Avg Step Speed Loss'],
            "aerobic_te": row['Aerobic TE'],
        }
        analysis["activities"].append(activity)
    
    return analysis


def print_analysis(analysis: dict) -> None:
    """Pretty print activity analysis."""
    print("\n📊 RUNNING PROFILE ANALYSIS")
    print("=" * 70)
    
    print(f"\n📈 Overall Statistics ({analysis['num_activities']} activities)")
    print("-" * 70)
    print(f"  Total Distance: {analysis['total_distance_km']:.1f} km")
    print(f"  Total Time: {analysis['total_time_hours']:.1f} hours")
    print(f"  Avg Pace: {analysis['avg_pace_min_km']:.1f} min/km")
    
    print("\n🏃 Running Cadence")
    print("-" * 70)
    print(f"  Avg: {analysis['avg_cadence']:.0f} spm")
    print(f"  Max: {analysis['max_cadence']:.0f} spm")
    print(f"  Min: {analysis['min_cadence']:.0f} spm")
    print(f"  Range: {analysis['cadence_range']:.0f} spm")
    
    print("\n❤️  Heart Rate")
    print("-" * 70)
    print(f"  Avg: {analysis['avg_hr']:.0f} bpm")
    print(f"  Max: {analysis['max_hr']:.0f} bpm")
    print(f"  Zone Efficiency: {analysis['hr_zone_efficiency']:.1f}% of max")
    
    print("\n🏃 Running Dynamics (Forerunner 970 + HRM-600)")
    print("-" * 70)
    print(f"  Avg Vertical Oscillation: {analysis['avg_vertical_oscillation']:.1f} cm")
    print(f"  Avg Vertical Ratio: {analysis['avg_vertical_ratio']:.2f}%")
    print(f"  Avg Ground Contact Time: {analysis['avg_ground_contact_time']:.0f} ms")
    print(f"  Avg Step Speed Loss: {analysis['avg_step_speed_loss_cms']:.1f} cm/s ({analysis['avg_step_speed_loss_pct']:.2f}%)")
    print(f"  Avg Stride Length: {analysis['avg_stride_length']:.2f} m")
    print(f"  Avg GCT Balance: {analysis['avg_gct_balance_left']:.1f}% L / {analysis['avg_gct_balance_right']:.1f}% R")
    
    print("\n⚡ Performance Metrics")
    print("-" * 70)
    print(f"  Avg Power: {analysis['avg_power']:.0f} watts")
    print(f"  Total Aerobic TE: {analysis['total_aerobic_te']:.1f}")
    print(f"  Avg Aerobic TE per run: {analysis['avg_aerobic_te']:.1f}")
    print(f"  Total Calories: {analysis['total_calories']:.0f}")
    
    print("\n📋 Recent Activities")
    print("-" * 70)
    for i, act in enumerate(analysis['activities'], 1):
        print(f"  {i}. {act['date']}")
        print(f"     {act['distance']:.1f}km | {act['time']} | HR {act['avg_hr']:.0f} | Cadence {act['cadence']:.0f}")
        print(f"     VO: {act['vertical_osc']:.1f}cm | GCT: {act['gct']:.0f}ms | SSL: {act['step_loss']:.1f}cm/s")


if __name__ == "__main__":
    """Analyze your Garmin Activities.csv."""
    print("🚀 Garmin Activities Analyzer")
    print("=" * 70)
    
    df = load_activities()
    if df.empty:
        print("❌ No Activities.csv found")
        print("📋 Copy your Garmin Activities.csv to data/Activities.csv")
        exit(1)
    
    analysis = analyze_activities(df)
    print_analysis(analysis)
    
    # Save analysis to JSON for later
    import json
    analysis_file = DATA_DIR / "running_profile.json"
    
    # Convert numpy types to native Python types for JSON serialization
    json_analysis = {}
    for k, v in analysis.items():
        if k != 'activities':
            # Convert numpy types to Python native types
            if isinstance(v, (np.integer, np.floating)):
                json_analysis[k] = float(v)
            else:
                json_analysis[k] = v
    
    with open(analysis_file, 'w') as f:
        json.dump(json_analysis, f, indent=2)
    
    print(f"\n💾 Profile saved: {analysis_file}")
