"""Synthetic Data Generator - Create training progression data."""
import json

import numpy as np
import pandas as pd

# from pathlib import Path
from .config import DATA_DIR

SYNTHETIC_DIR = DATA_DIR / "synthetic"
SYNTHETIC_DIR.mkdir(exist_ok=True)


def load_current_profile():
    """Load current running profile."""
    profile_file = DATA_DIR / "running_profile.json"
    if not profile_file.exists():
        print(f"❌ {profile_file} not found")
        return None
    
    with open(profile_file, 'r') as f:
        return json.load(f)


def load_target_profiles():
    """Load target runner profiles."""
    profiles_file = DATA_DIR / "target_profiles.json"
    if not profiles_file.exists():
        print(f"❌ {profiles_file} not found")
        return None
    
    with open(profiles_file, 'r') as f:
        return json.load(f)


def interpolate_metric(current: float, target: float, weeks: int = 16, noise_level: float = 0.05) -> list:
    """
    Interpolate metric from current to target over N weeks.
    
    Args:
        current: Starting value
        target: Target value
        weeks: Number of weeks to progress
        noise_level: Variance (0.05 = ±5%)
    
    Returns:
        List of weekly values with realistic noise
    """
    values = []
    
    for week in range(1, weeks + 1):
        # Linear interpolation
        progress = week / weeks
        value = current + (target - current) * progress
        
        # Add realistic noise (varies by week, more stable in later weeks)
        noise_std = noise_level * abs(current - target) * (1 - progress * 0.5)
        noise = np.random.normal(0, noise_std)
        
        value_with_noise = value + noise
        values.append(round(value_with_noise, 2))
    
    return values


def generate_synthetic_progression(current: dict, target_profile: dict, 
                                 num_weeks: int = 16, runs_per_week: int = 3) -> pd.DataFrame:
    """Generate synthetic runs showing progression toward target."""
    
    synthetic_runs = []
    
    # Define metrics to interpolate
    metric_mappings = {
        "cadence_spm": ("avg_cadence", "cadence_spm"),
        "vertical_oscillation_cm": ("avg_vertical_oscillation", "vertical_oscillation_cm"),
        "ground_contact_time_ms": ("avg_ground_contact_time", "ground_contact_time_ms"),
        "step_speed_loss_pct": ("avg_step_speed_loss_pct", "step_speed_loss_percent"),
        "heart_rate_bpm": ("avg_hr", "hr_efficiency"),  # Will handle separately
    }
    
    # Generate interpolated progressions for each metric
    progressions = {}
    
    for metric_key, (current_key, target_key) in metric_mappings.items():
        if current_key in current and target_key in target_profile["metrics"]:
            current_val = current[current_key]
            target_val = target_profile["metrics"][target_key]["ideal"]
            
            progressions[metric_key] = interpolate_metric(
                current_val, target_val, weeks=num_weeks, noise_level=0.08
            )
    
    # Generate synthetic runs
    run_id = 1000
    for week in range(1, num_weeks + 1):
        for day in range(runs_per_week):
            run_id += 1
            
            # Get values for this week
            run_data = {
                "activity_id": f"synthetic_{run_id}",
                "week": week,
                "day": day + 1,
                "date": f"2025-{(week % 52 + 1):02d}-{(day + 1) * 2:02d}",
                "distance_km": round(np.random.uniform(4, 12), 2),
                "duration_min": round(np.random.uniform(30, 80), 1),
            }
            
            # Add progressive metrics
            for metric_key, values in progressions.items():
                run_data[metric_key] = values[week - 1] if week <= len(values) else values[-1]
            
            # Add pace (derived from distance/duration)
            pace = run_data["duration_min"] / run_data["distance_km"]
            run_data["pace_min_km"] = round(pace, 2)
            
            # Add power (derived from HR and cadence)
            estimated_power = 200 + (run_data.get("cadence_spm", 170) - 160) * 2 + \
                            (run_data.get("heart_rate_bpm", 150) - 140) * 0.5
            run_data["power_watts"] = round(estimated_power, 0)
            
            # Add training effect based on metrics
            te = 1.5 + (run_data.get("heart_rate_bpm", 150) - 140) * 0.05
            run_data["aerobic_te"] = round(min(5.0, max(1.0, te)), 1)
            
            # Label: current vs improved
            improvement = (run_data["cadence_spm"] - progressions["cadence_spm"][0]) / \
                         (progressions["cadence_spm"][-1] - progressions["cadence_spm"][0] + 0.001)
            run_data["improvement_phase"] = "early" if improvement < 0.33 else \
                                           "mid" if improvement < 0.67 else "advanced"
            
            synthetic_runs.append(run_data)
    
    return pd.DataFrame(synthetic_runs)


def generate_all_profiles(current: dict, targets: dict, output_csv: bool = True) -> dict:
    """Generate synthetic data for all target profiles."""
    
    results = {}
    
    for profile_key, profile in targets.items():
        print(f"🔄 Generating {profile['name']} progression...")
        
        df = generate_synthetic_progression(current, profile, num_weeks=16, runs_per_week=3)
        
        if output_csv:
            csv_path = SYNTHETIC_DIR / f"synthetic_{profile_key}.csv"
            df.to_csv(csv_path, index=False)
            print(f"   ✅ Saved {len(df)} synthetic runs to {csv_path.name}")
        
        results[profile_key] = {
            "profile_name": profile["name"],
            "num_runs": len(df),
            "weeks": 16,
            "dataframe": df
        }
    
    return results


def print_sample(df: pd.DataFrame, profile_name: str) -> None:
    """Print sample of synthetic data."""
    print(f"\n📋 SAMPLE: {profile_name}")
    print("-" * 100)
    
    # Show progression across weeks
    weeks = df["week"].unique()
    sample_weeks = [weeks[0], weeks[len(weeks)//2], weeks[-1]]
    
    for week in sample_weeks:
        week_data = df[df["week"] == week].iloc[0]
        print(f"\nWeek {int(week)}:")
        print(f"  Cadence: {week_data['cadence_spm']:.0f} spm")
        print(f"  VO: {week_data['vertical_oscillation_cm']:.1f} cm")
        print(f"  GCT: {week_data['ground_contact_time_ms']:.0f} ms")
        print(f"  SSL: {week_data['step_speed_loss_pct']:.2f}%")
        print(f"  HR: {week_data['heart_rate_bpm']:.0f} bpm")
        print(f"  Pace: {week_data['pace_min_km']:.2f} min/km")


def print_summary(results: dict) -> None:
    """Print summary of synthetic data generation."""
    print("\n" + "=" * 100)
    print("✅ SYNTHETIC DATA GENERATION COMPLETE")
    print("=" * 100)
    
    for profile_key, result in results.items():
        print(f"\n🎯 {result['profile_name']}")
        print(f"   Weeks: {result['weeks']}")
        print(f"   Total synthetic runs: {result['num_runs']}")
        print("   Runs per week: 3")
        print(f"   File: synthetic_{profile_key}.csv")
        
        # Show metric progressions
        df = result["dataframe"]
        first_week = df[df["week"] == 1].iloc[0]
        last_week = df[df["week"] == df["week"].max()].iloc[0]
        
        print("\n   Progression (Week 1 → Week 16):")
        print(f"   • Cadence: {first_week['cadence_spm']:.0f} → {last_week['cadence_spm']:.0f} spm "
              f"(+{last_week['cadence_spm'] - first_week['cadence_spm']:.1f})")
        print(f"   • VO: {first_week['vertical_oscillation_cm']:.1f} → {last_week['vertical_oscillation_cm']:.1f} cm "
              f"({last_week['vertical_oscillation_cm'] - first_week['vertical_oscillation_cm']:+.1f})")
        print(f"   • GCT: {first_week['ground_contact_time_ms']:.0f} → {last_week['ground_contact_time_ms']:.0f} ms "
              f"({last_week['ground_contact_time_ms'] - first_week['ground_contact_time_ms']:+.0f})")
        print(f"   • SSL: {first_week['step_speed_loss_pct']:.2f}% → {last_week['step_speed_loss_pct']:.2f}% "
              f"({last_week['step_speed_loss_pct'] - first_week['step_speed_loss_pct']:+.2f}%)")


if __name__ == "__main__":
    """Generate synthetic training progression data."""
    print("🚀 Synthetic Data Generator")
    print("=" * 100)
    
    # Load current and target data
    current = load_current_profile()
    targets = load_target_profiles()
    
    if current is None or targets is None:
        print("❌ Failed to load profiles")
        exit(1)
    
    print("✅ Loaded current profile")
    print(f"✅ Loaded {len(targets)} target profiles")
    
    # Generate synthetic data for all profiles
    results = generate_all_profiles(current, targets, output_csv=True)
    
    # Print samples
    for profile_key, result in results.items():
        print_sample(result["dataframe"], result["profile_name"])
    
    # Print summary
    print_summary(results)
    
    # Save master synthetic dataset (all profiles combined)
    all_synthetic = []
    for profile_key, result in results.items():
        df = result["dataframe"].copy()
        df["target_profile"] = result["profile_name"]
        all_synthetic.append(df)
    
    master_df = pd.concat(all_synthetic, ignore_index=True)
    master_file = SYNTHETIC_DIR / "synthetic_all_profiles.csv"
    master_df.to_csv(master_file, index=False)
    
    print(f"\n💾 Master synthetic dataset: {master_file.name} ({len(master_df)} total runs)")
    print("=" * 100 + "\n")
