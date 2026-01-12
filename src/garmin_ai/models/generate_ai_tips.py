# generate_ai_tips.py - FIXED: Use gaps (now accessed!)
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import json

from config import DATA_DIR
from predict_form_gaps import (
    get_latest_activity_data,
    load_model_components,
    predict_new_run,
)

DRILLS = {
    'cadencespm': ["Metronome 170spm 10x1min", "High-knee 3x30s", "8x200m tempo"], 
    'verticaloscillationcm': ["Light footstrike 10x20s", "Calf raises 4x15", "Pogo 3x20s"],
    'groundcontacttimems': ["Bounding 6x30m", "Box jumps 4x10", "Ski hops 3x20s"],
    'stepspeedlosspct': ["Hill repeats 8x30s", "Single-leg hops 3x15", "A-skips 4x40m"],
    'paceminkm': ["Tempo 20min", "Fartlek 30min", "Strides 10x20s"]
}

def generate_tips(results: dict) -> list:
    """Generate personalized 4-week plan."""
    tips = [f"🎯 FORM: {results['form_score']}/100"]
    gaps = results['gaps']  # ✅ NOW USED!
    priorities = results['priority_gaps']
    
    score = results['form_score']
    if score > 85: 
        tips.append("✅ Elite!")
    elif score > 70: 
        tips.append("📈 Good - fix gaps.")
    else: 
        tips.append("🔧 Big potential!")
    
    # ✅ USE gaps data!
    for week, (metric, gap_data) in enumerate(priorities, 1):
        drill_key = metric.split('cm')[0].split('ms')[0]  # Clean key
        drill = DRILLS.get(drill_key, DRILLS['stepspeedlosspct'])[0]
        
        gap_val = gaps[metric]['gap']  # ✅ gaps accessed here!
        metric_name = metric.replace('stepspeedlosspct', 'SSL').replace('paceminkm', 'Pace')
        
        tips.extend([
            f"\n📅 WEEK {week}: {metric_name}",
            f"   Current: {gap_data['current']:.1f}",
            f"   Target: {gap_data['target']:.1f}",
            f"   Gap: {gap_val:+.1f}",
            f"   Drill: {drill}"
        ])
    
    tips.append("\n📱 Log in Garmin → re-analyze weekly!")
    return tips

if __name__ == "__main__":
    print("🤖 AI RUNNING PLAN")
    print("=" * 30)
    
    model, scaler, feature_cols = load_model_components()
    df, latest = get_latest_activity_data()
    results = predict_new_run(df, latest, model, scaler, feature_cols)
    tips = generate_tips(results)
    
    for tip in tips:
        print(tip)
    
    # Save full analysis
    output = {
        "form_score": results['form_score'],
        "gaps": results['gaps'],  # ✅ Include raw gaps
        "priority_gaps": results['priority_gaps'],
        "tips": tips,
        "date": results['activity_date']
    }
    with open(DATA_DIR / "ai_tips.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n💾 {DATA_DIR}/ai_tips.json")
