"""Form Analyzer - Score your running form against benchmarks."""
import json

import pandas as pd

from .config import DATA_DIR

ACTIVITIES_CSV = DATA_DIR / "Activities.csv"
RUNNING_PROFILE = DATA_DIR / "running_profile.json"


# Sports science benchmarks for 50-year-old runners
BENCHMARKS = {
    "cadence_spm": {
        "elite": {"min": 180, "max": 200},
        "good": {"min": 165, "max": 180},
        "target": {"min": 165, "max": 180},
        "description": "Steps per minute"
    },
    "vertical_oscillation_cm": {
        "elite": {"min": 0, "max": 7},
        "good": {"min": 7, "max": 9},
        "target": {"min": 7, "max": 8},
        "description": "Vertical bounce (cm) - lower is better"
    },
    "vertical_ratio": {
        "elite": {"min": 0, "max": 7},
        "good": {"min": 7, "max": 9},
        "target": {"min": 7, "max": 8.5},
        "description": "Vertical movement ratio (%) - lower is better"
    },
    "ground_contact_time_ms": {
        "elite": {"min": 200, "max": 240},
        "good": {"min": 240, "max": 280},
        "target": {"min": 240, "max": 270},
        "description": "Ground contact time (ms) - shorter is better"
    },
    "step_speed_loss_percent": {
        "elite": {"min": 0, "max": 4},
        "good": {"min": 4, "max": 8},
        "target": {"min": 4, "max": 6},
        "description": "Step speed loss (%) - lower is better"
    },
    "hr_efficiency": {
        "elite": {"min": 85, "max": 100},
        "good": {"min": 75, "max": 85},
        "target": {"min": 75, "max": 90},
        "description": "HR as % of max (lower = more efficient)"
    }
}


def load_data():
    """Load Activities.csv and running_profile.json."""
    if not ACTIVITIES_CSV.exists():
        print(f"❌ {ACTIVITIES_CSV} not found")
        return None, None
    if not RUNNING_PROFILE.exists():
        print(f"❌ {RUNNING_PROFILE} not found")
        return None, None
    
    df = pd.read_csv(ACTIVITIES_CSV)
    with open(RUNNING_PROFILE, 'r') as f:
        profile = json.load(f)
    
    return df, profile


def score_metric(value, benchmark_key: str) -> dict:
    """Score a metric against benchmarks (0-100)."""
    bench = BENCHMARKS[benchmark_key]
    elite_range = bench["elite"]
    good_range = bench["good"]
    target_range = bench["target"]
    
    # For metrics where "lower is better" (VO, SSL, GCT)
    if "lower" in bench["description"].lower():
        if elite_range["min"] <= value <= elite_range["max"]:
            score = 100
        elif good_range["min"] <= value <= good_range["max"]:
            # Scale from 70-100 in good range
            range_size = good_range["max"] - good_range["min"]
            position = (value - good_range["min"]) / range_size
            score = 70 + (position * 30)
        elif value < elite_range["min"]:
            score = 100  # Better than elite
        else:
            # Worse than good range
            score = max(30, 70 - (value - good_range["max"]) * 5)
    else:
        # For metrics where "higher is better" (cadence, HR efficiency)
        if elite_range["min"] <= value <= elite_range["max"]:
            score = 100
        elif target_range["min"] <= value <= target_range["max"]:
            range_size = target_range["max"] - target_range["min"]
            position = (value - target_range["min"]) / range_size
            score = 75 + (position * 25)
        elif value < target_range["min"]:
            score = max(30, 75 - (target_range["min"] - value) * 2)
        else:
            score = max(0, 75 - (value - target_range["max"]) * 3)
    
    return {
        "value": round(value, 2),
        "score": round(max(0, min(100, score)), 1),
        "benchmark": bench,
        "status": "⭐ Elite" if score >= 95 else "✅ Good" if score >= 75 else "🎯 Target" if score >= 60 else "⚠️ Develop"
    }


def analyze_form(df: pd.DataFrame, profile: dict) -> dict:
    """Comprehensive form analysis."""
    analysis = {
        "timestamp": pd.Timestamp.now().isoformat(),
        "num_activities": len(df),
        
        # Individual metric scores
        "metrics": {},
        
        # Summary scores
        "overall_score": 0,
        "strengths": [],
        "improvement_areas": [],
        "recommendations": []
    }
    
    # Score cadence
    cadence = profile["avg_cadence"]
    analysis["metrics"]["cadence"] = score_metric(cadence, "cadence_spm")
    
    # Score vertical oscillation
    vo = profile["avg_vertical_oscillation"]
    analysis["metrics"]["vertical_oscillation"] = score_metric(vo, "vertical_oscillation_cm")
    
    # Score vertical ratio
    vr = profile["avg_vertical_ratio"]
    analysis["metrics"]["vertical_ratio"] = score_metric(vr, "vertical_ratio")
    
    # Score ground contact time
    gct = profile["avg_ground_contact_time"]
    analysis["metrics"]["ground_contact_time"] = score_metric(gct, "ground_contact_time_ms")
    
    # Score step speed loss
    ssl = profile["avg_step_speed_loss_pct"]
    analysis["metrics"]["step_speed_loss"] = score_metric(ssl, "step_speed_loss_percent")
    
    # Score HR efficiency (avg HR / max HR * 100)
    hr_eff = (profile["avg_hr"] / profile["max_hr"]) * 100
    analysis["metrics"]["hr_efficiency"] = score_metric(hr_eff, "hr_efficiency")
    
    # Calculate overall score (weighted average)
    weights = {
        "cadence": 0.15,
        "vertical_oscillation": 0.20,
        "ground_contact_time": 0.20,
        "step_speed_loss": 0.25,
        "hr_efficiency": 0.20
    }
    
    overall = sum(
        analysis["metrics"][key]["score"] * weights[key] 
        for key in weights
    )
    analysis["overall_score"] = round(overall, 1)
    
    # Identify strengths (score >= 80)
    for metric_name, metric_data in analysis["metrics"].items():
        if metric_data["score"] >= 80:
            analysis["strengths"].append({
                "metric": metric_name.replace("_", " ").title(),
                "score": metric_data["score"],
                "value": metric_data["value"]
            })
        elif metric_data["score"] < 70:
            analysis["improvement_areas"].append({
                "metric": metric_name.replace("_", " ").title(),
                "score": metric_data["score"],
                "value": metric_data["value"],
                "target": metric_data["benchmark"]["target"]
            })
    
    # Generate recommendations
    recommendations = {
        "cadence": {
            "issue": cadence < 165,
            "suggestion": f"Increase cadence from {cadence:.0f} to 170+ spm using metronome drills"
        },
        "step_speed_loss": {
            "issue": ssl > 7,
            "suggestion": "Reduce SSL with hill repeats and lower-body strength training"
        },
        "vertical_oscillation": {
            "issue": vo > 8.5,
            "suggestion": "Improve VO with lighter footstrike drills and calf strengthening"
        },
        "ground_contact_time": {
            "issue": gct > 280,
            "suggestion": "Shorten GCT with plyometric training and explosive leg work"
        }
    }
    
    for metric, rec in recommendations.items():
        if rec["issue"]:
            analysis["recommendations"].append(rec["suggestion"])
    
    return analysis


def print_report(analysis: dict) -> None:
    """Pretty print form analysis report."""
    print("\n" + "=" * 80)
    print("📊 RUNNING FORM ANALYSIS REPORT")
    print("=" * 80)
    
    # Overall score
    score = analysis["overall_score"]
    if score >= 85:
        rating = "🌟 EXCELLENT"
    elif score >= 75:
        rating = "✅ GOOD"
    elif score >= 60:
        rating = "🎯 DEVELOPING"
    else:
        rating = "⚠️ NEEDS WORK"
    
    print(f"\n🎯 OVERALL FORM SCORE: {score}/100 {rating}")
    print(f"   Based on {analysis['num_activities']} activities")
    
    # Individual metrics
    print("\n📋 DETAILED METRICS")
    print("-" * 80)
    for metric_name, metric_data in analysis["metrics"].items():
        _ = metric_name.replace("_", " ").title()
        bench = metric_data["benchmark"]
        print(f"\n  {metric_name.upper()}: {metric_data['score']}/100 {metric_data['status']}")
        print(f"    Current: {metric_data['value']}")
        print(f"    Target: {bench['target']['min']}-{bench['target']['max']}")
        print(f"    → {bench['description']}")
    
    # Strengths
    if analysis["strengths"]:
        print(f"\n✅ STRENGTHS ({len(analysis['strengths'])})")
        print("-" * 80)
        for strength in analysis["strengths"]:
            print(f"  ⭐ {strength['metric']}: {strength['score']}/100 (value: {strength['value']})")
    
    # Improvement areas
    if analysis["improvement_areas"]:
        print(f"\n🎯 FOCUS AREAS ({len(analysis['improvement_areas'])})")
        print("-" * 80)
        for area in analysis["improvement_areas"]:
            target = area["target"]
            print(f"  📌 {area['metric']}: {area['score']}/100")
            print(f"     Current: {area['value']}")
            print(f"     Target: {target['min']}-{target['max']}")
    
    # Recommendations
    if analysis["recommendations"]:
        print("\n💡 TRAINING RECOMMENDATIONS")
        print("-" * 80)
        for i, rec in enumerate(analysis["recommendations"], 1):
            print(f"  {i}. {rec}")
    
    # Next steps
    print("\n📅 NEXT 4 WEEKS")
    print("-" * 80)
    print("  Week 1-2: Focus on top priority (usually cadence or step speed loss)")
    print("  Week 3-4: Add secondary focus with strength training")
    print("  Each week: Track metrics to monitor improvement")
    
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    """Run form analyzer."""
    print("🚀 Running Form Analyzer")
    print("=" * 80)
    
    df, profile = load_data()
    if df is None or profile is None:
        print("❌ Failed to load data")
        print(f"   Ensure {ACTIVITIES_CSV} and {RUNNING_PROFILE} exist")
        exit(1)
    
    print(f"✅ Loaded {len(df)} activities")
    print(f"✅ Loaded running profile with {len(profile)} metrics")
    
    # Analyze
    analysis = analyze_form(df, profile)
    
    # Print report
    print_report(analysis)
    
    # Save results
    output_file = DATA_DIR / "form_analysis.json"
    with open(output_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"💾 Analysis saved: {output_file}")
