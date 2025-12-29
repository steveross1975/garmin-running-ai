"""Target Profiles - Define experienced 50yo runner archetypes."""
import json

from .config import DATA_DIR

TARGET_PROFILES = {
    "steady_runner": {
        "name": "Steady Runner",
        "description": "Conservative, focus on endurance and consistency",
        "archetype": "Marathon-focused, injury-preventive approach",
        "metrics": {
            "cadence_spm": {
                "min": 155,
                "max": 165,
                "ideal": 160,
                "description": "Lower cadence, longer stride"
            },
            "vertical_oscillation_cm": {
                "min": 7.0,
                "max": 8.0,
                "ideal": 7.5,
                "description": "Good bounce control"
            },
            "vertical_ratio": {
                "min": 7.0,
                "max": 8.0,
                "ideal": 7.5,
                "description": "Efficient vertical movement"
            },
            "ground_contact_time_ms": {
                "min": 250,
                "max": 260,
                "ideal": 255,
                "description": "Moderate contact time"
            },
            "step_speed_loss_percent": {
                "min": 5.0,
                "max": 6.0,
                "ideal": 5.5,
                "description": "Low energy loss per step"
            },
            "hr_efficiency": {
                "min": 75,
                "max": 85,
                "ideal": 80,
                "description": "Conservative HR zones"
            }
        },
        "training_focus": [
            "Long, steady runs (60-90 min)",
            "Easy recovery runs",
            "Occasional tempo runs (20-30 min)",
            "Strength: 1x/week (maintenance)"
        ],
        "target_pace_min_km": 5.45,
        "target_max_hr": 170
    },
    
    "efficient_runner": {
        "name": "Efficient Runner",
        "description": "Optimized form, focus on running economy",
        "archetype": "Speed-focused, biomechanically efficient",
        "metrics": {
            "cadence_spm": {
                "min": 170,
                "max": 180,
                "ideal": 175,
                "description": "Higher cadence, shorter stride"
            },
            "vertical_oscillation_cm": {
                "min": 7.0,
                "max": 7.5,
                "ideal": 7.2,
                "description": "Minimal bounce"
            },
            "vertical_ratio": {
                "min": 7.0,
                "max": 7.5,
                "ideal": 7.2,
                "description": "Very efficient movement"
            },
            "ground_contact_time_ms": {
                "min": 240,
                "max": 250,
                "ideal": 245,
                "description": "Short contact time"
            },
            "step_speed_loss_percent": {
                "min": 4.0,
                "max": 5.0,
                "ideal": 4.5,
                "description": "Minimal energy loss"
            },
            "hr_efficiency": {
                "min": 78,
                "max": 88,
                "ideal": 83,
                "description": "Optimized zone efficiency"
            }
        },
        "training_focus": [
            "Tempo runs (30-40 min)",
            "Interval training (6-8 x 3-5min)",
            "Speed work (fartlek, strides)",
            "Strength: 2x/week (explosive)"
        ],
        "target_pace_min_km": 5.15,
        "target_max_hr": 172
    },
    
    "balanced_runner": {
        "name": "Balanced Runner",
        "description": "Mix of speed and endurance, versatile training",
        "archetype": "All-around, adaptable to different race distances",
        "metrics": {
            "cadence_spm": {
                "min": 165,
                "max": 175,
                "ideal": 170,
                "description": "Moderate-high cadence"
            },
            "vertical_oscillation_cm": {
                "min": 7.5,
                "max": 8.5,
                "ideal": 8.0,
                "description": "Good bounce control"
            },
            "vertical_ratio": {
                "min": 7.5,
                "max": 8.5,
                "ideal": 8.0,
                "description": "Balanced efficiency"
            },
            "ground_contact_time_ms": {
                "min": 250,
                "max": 270,
                "ideal": 260,
                "description": "Balanced contact"
            },
            "step_speed_loss_percent": {
                "min": 5.0,
                "max": 7.0,
                "ideal": 6.0,
                "description": "Moderate energy efficiency"
            },
            "hr_efficiency": {
                "min": 76,
                "max": 86,
                "ideal": 81,
                "description": "Balanced zone distribution"
            }
        },
        "training_focus": [
            "Mix of easy and tempo runs",
            "Occasional speed work (8-10 x 2-3min)",
            "Medium-long runs (45-75 min)",
            "Strength: 2x/week (balanced)"
        ],
        "target_pace_min_km": 5.30,
        "target_max_hr": 171
    }
}


def compare_to_profiles(current_metrics: dict) -> dict:
    """Compare current metrics to all target profiles."""
    comparison = {
        "current": current_metrics,
        "profiles": {}
    }
    
    for profile_key, profile in TARGET_PROFILES.items():
        profile_comparison = {
            "name": profile["name"],
            "description": profile["description"],
            "metrics_distance": 0,
            "metric_deltas": {}
        }
        
        # Compare each metric
        num_metrics = 0
        for metric_name, metric_range in profile["metrics"].items():
            if metric_name in current_metrics:
                current_value = current_metrics[metric_name]
                ideal_value = metric_range["ideal"]
                delta = current_value - ideal_value
                
                profile_comparison["metric_deltas"][metric_name] = {
                    "current": round(current_value, 2),
                    "target": round(ideal_value, 2),
                    "delta": round(delta, 2),
                    "delta_percent": round((delta / ideal_value * 100), 1) if ideal_value != 0 else 0
                }
                
                profile_comparison["metrics_distance"] += abs(delta)
                num_metrics += 1
        
        # Average distance
        if num_metrics > 0:
            profile_comparison["avg_metric_distance"] = round(
                profile_comparison["metrics_distance"] / num_metrics, 2
            )
        
        # Recommendation
        if profile_comparison["metrics_distance"] < 2.0:
            profile_comparison["fit"] = "🎯 EXCELLENT FIT"
        elif profile_comparison["metrics_distance"] < 3.5:
            profile_comparison["fit"] = "✅ GOOD FIT"
        else:
            profile_comparison["fit"] = "⚠️ SIGNIFICANT CHANGES NEEDED"
        
        comparison["profiles"][profile_key] = profile_comparison
    
    return comparison


def print_profiles() -> None:
    """Pretty print all target profiles."""
    print("\n" + "=" * 80)
    print("🎯 TARGET RUNNER PROFILES (50-year-old experienced runners)")
    print("=" * 80)
    
    for profile_key, profile in TARGET_PROFILES.items():
        print(f"\n📌 {profile['name'].upper()}")
        print(f"   {profile['description']}")
        print(f"   Type: {profile['archetype']}")
        
        print("\n   Metrics:")
        for metric_name, metric_range in profile["metrics"].items():
            print(f"   • {metric_name.replace('_', ' ').title()}: "
                  f"{metric_range['min']}-{metric_range['max']} "
                  f"(ideal: {metric_range['ideal']})")
        
        print("\n   Training Focus:")
        for focus in profile["training_focus"]:
            print(f"   • {focus}")
        
        print("\n   Expected Performance:")
        print(f"   • Target Pace: {profile['target_pace_min_km']:.2f} min/km")
        print(f"   • Max HR: {profile['target_max_hr']} bpm")
        print("-" * 80)


def print_comparison(current_metrics: dict) -> None:
    """Print comparison of current metrics to profiles."""
    comparison = compare_to_profiles(current_metrics)
    
    print("\n" + "=" * 80)
    print("📊 YOUR PROFILE COMPARISON")
    print("=" * 80)
    
    # Find best fit
    best_fit = min(
        comparison["profiles"].items(),
        key=lambda x: x[1]["metrics_distance"]
    )
    
    print(f"\n🏃 BEST FIT: {best_fit[1]['name']} {best_fit[1]['fit']}")
    print(f"   Distance from ideal: {best_fit[1]['avg_metric_distance']}")
    
    # Show deltas
    print("\n📋 METRIC COMPARISON:")
    print("-" * 80)
    
    for metric_name, delta_info in best_fit[1]["metric_deltas"].items():
        symbol = "✅" if abs(delta_info["delta"]) < 0.5 else "→" if abs(delta_info["delta"]) < 1.5 else "⚠️"
        print(f"{symbol} {metric_name.replace('_', ' ').title()}")
        print(f"   Current: {delta_info['current']} | Target: {delta_info['target']} "
              f"| Gap: {delta_info['delta_percent']:+.1f}%")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    """Test target profiles."""
    print("🚀 Target Runner Profiles")
    print("=" * 80)
    
    # Print all profiles
    print_profiles()
    
    # Example: Load current metrics and compare
    profile_file = DATA_DIR / "running_profile.json"
    if profile_file.exists():
        with open(profile_file, 'r') as f:
            current = json.load(f)
        
        # Extract key metrics
        current_metrics = {
            "cadence_spm": current.get("avg_cadence", 0),
            "vertical_oscillation_cm": current.get("avg_vertical_oscillation", 0),
            "vertical_ratio": current.get("avg_vertical_ratio", 0),
            "ground_contact_time_ms": current.get("avg_ground_contact_time", 0),
            "step_speed_loss_percent": current.get("avg_step_speed_loss_pct", 0),
            "hr_efficiency": (current.get("avg_hr", 0) / current.get("max_hr", 1)) * 100
        }
        
        print_comparison(current_metrics)
        
        # Save profiles
        profiles_file = DATA_DIR / "target_profiles.json"
        with open(profiles_file, 'w') as f:
            json.dump(TARGET_PROFILES, f, indent=2)
        print(f"\n💾 Profiles saved: {profiles_file}")
