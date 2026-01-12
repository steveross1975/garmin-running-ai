"""Analyze Garmin Activities.csv - comprehensive running metrics."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from config import DATA_DIR

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
        return 0.0
    except Exception:
        return 0.0

def parse_gct_balance(balance_str: str) -> tuple:
    """Parse GCT Balance like '50.1% L / 49.9% R' to (left%, right%)."""
    try:
        parts = str(balance_str).replace('%', '').split('/')
        left = float(parts[0].strip().replace('L', ''))
        right = float(parts[1].strip().replace('R', ''))
        return (float(left), float(right))
    except Exception:
        return (50.0, 50.0)

def to_python_native(value):
    """Convert numpy/pandas types to Python native types."""
    if pd.isna(value):
        return 0.0
    if isinstance(value, (np.integer, np.int64, np.int32)):
        return int(value)
    if isinstance(value, (np.floating, np.float64, np.float32)):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value

def analyze_activities(df: pd.DataFrame) -> dict:
    """Comprehensive analysis of all running activities - JSON SAFE."""
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
    
    # Convert ALL pandas series to Python floats FIRST
    def safe_mean(series):
        return float(series.mean()) if not series.empty else 0.0
    
    def safe_sum(series):
        return float(series.sum()) if not series.empty else 0.0
    
    def safe_max(series):
        return float(series.max()) if not series.empty else 0.0
    
    def safe_min(series):
        return float(series.min()) if not series.empty else 0.0
    
    analysis = {
        "num_activities": int(len(df)),
        "total_distance_km": safe_sum(df['Distance']),
        "total_time_hours": safe_sum(df_clean['Time_Seconds']) / 3600,
        
        # Running Cadence
        "avg_cadence": safe_mean(df['Avg Run Cadence']),
        "max_cadence": safe_max(df['Max Run Cadence']),
        "min_cadence": safe_min(df['Avg Run Cadence']),
        "cadence_range": safe_max(df['Max Run Cadence']) - safe_min(df['Avg Run Cadence']),
        
        # Heart Rate
        "avg_hr": safe_mean(df['Avg HR']),
        "max_hr": safe_max(df['Max HR']),
        "min_hr": safe_min(df['Avg HR']),
        "hr_zone_efficiency": safe_mean(df['Avg HR']) / safe_max(df['Max HR']) * 100 if safe_max(df['Max HR']) > 0 else 0.0,
        
        # Running Dynamics
        "avg_vertical_oscillation": safe_mean(df['Avg Vertical Oscillation']),
        "avg_vertical_ratio": safe_mean(df['Avg Vertical Ratio']),
        "avg_ground_contact_time": safe_mean(df['Avg Ground Contact Time']),
        "avg_step_speed_loss_cms": safe_mean(df['Avg Step Speed Loss']),
        "avg_step_speed_loss_pct": safe_mean(df['Avg Step Speed Loss %']),
        "avg_stride_length": safe_mean(df['Avg Stride Length']),
        
        # GCT Balance (left/right)
        "avg_gct_balance_left": safe_mean(df_clean['GCT_Balance_Left']),
        "avg_gct_balance_right": safe_mean(df_clean['GCT_Balance_Right']),
        
        # Pace & Power
        "avg_pace_min_km": safe_mean(df['Avg Pace'].astype(str).str.split(':').apply(
            lambda x: (int(x[0]) * 60 + int(x[1])) / 60 if len(x) == 2 else 0.0
        )),
        "avg_power": safe_mean(df['Avg Power']),
        
        # Training Metrics
        "total_aerobic_te": safe_sum(df['Aerobic TE']),
        "avg_aerobic_te": safe_mean(df['Aerobic TE']),
        "total_calories": safe_sum(df['Calories']),
        
        # Activity Details
        "activities": []
    }
    
    # Per-activity details - ALL Python native
    for idx, row in df.iterrows():
        activity = {
            "date": str(row['Date']),
            "distance": float(row['Distance']),
            "time": str(row['Time']),
            "avg_hr": float(row['Avg HR']),
            "cadence": float(row['Avg Run Cadence']),
            "vertical_osc": float(row['Avg Vertical Oscillation']),
            "gct": float(row['Avg Ground Contact Time']),
            "step_loss": float(row['Avg Step Speed Loss']),
            "aerobic_te": float(row['Aerobic TE']),
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

def create_running_profile(analysis):
    """Create running profile JSON from analysis dict - already Python native."""
    return {
        'avg_cadence': float(analysis.get('avg_cadence', 0)),
        'avg_hr': float(analysis.get('avg_hr', 0)),
        'max_hr': float(analysis.get('max_hr', 0)),
        'avg_vertical_oscillation': float(analysis.get('avg_vertical_oscillation', 0)),
        'avg_vertical_ratio': float(analysis.get('avg_vertical_ratio', 0)),
        'avg_ground_contact_time': float(analysis.get('avg_ground_contact_time', 0)),
        'avg_step_speed_loss': float(analysis.get('avg_step_speed_loss_cms', 0)),
        'avg_step_speed_loss_pct': float(analysis.get('avg_step_speed_loss_pct', 0)),
        'avg_stride_length': float(analysis.get('avg_stride_length', 0)),
        'avg_gct_balance_left': float(analysis.get('avg_gct_balance_left', 50)),
        'avg_gct_balance_right': float(analysis.get('avg_gct_balance_right', 50)),
        'avg_pace_min_km': float(analysis.get('avg_pace_min_km', 0)),
        'avg_power': float(analysis.get('avg_power', 0)),
        'total_aerobic_te': float(analysis.get('total_aerobic_te', 0)),
        'avg_aerobic_te': float(analysis.get('avg_aerobic_te', 0)),
    }

def save_running_profile(profile, path=None):
    """Save running profile - simplified (data already JSON safe)."""
    if path is None:
        path = DATA_DIR / 'running_profile.json'
    
    with open(path, 'w') as f:
        json.dump(profile, f, indent=2)
    
    print(f"✅ Saved {path}")
    return path

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
    running_profile = create_running_profile(analysis)
    print("🔍 DEBUG: running_profile types =", {k: type(v).__name__ for k, v in running_profile.items()})
    print("🔍 DEBUG: sample values =", list(running_profile.items())[:3])
    try:
        test_json = json.dumps(running_profile)
        print("✅ JSON serializable OK!")
    except Exception as e:
        print(f"❌ JSON ERROR: {e}")
        import traceback
        traceback.print_exc()
    save_running_profile(running_profile)
