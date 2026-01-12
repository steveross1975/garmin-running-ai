# predict_form_gaps.py - FULLY FIXED for your exact config/version
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import json

import joblib
import numpy as np
import pandas as pd
from config import ACTIVITIES_CSV, DATA_DIR, MODELS_DIR  # ✅ Your snake_case names


# ✅ SAFE PACE PARSER (fixes "5:51" error)
def parse_garmin_pace(pace_str):
    """FIXED: '5:51' → 5.85 min/km."""
    if pd.isna(pace_str):
        return 5.5
    s = str(pace_str).strip()
    if ':' in s:
        parts = s.split(':')
        minutes = int(parts[0])
        seconds = int(parts[1]) / 60.0  # ✅ FIXED: /60.0 !
        return minutes + seconds
    return float(s) if s else 5.5


def load_model_components():
    """Load trained model."""
    model = joblib.load(MODELS_DIR / 'form_predictor_model.pkl')
    scaler = joblib.load(MODELS_DIR / 'feature_scaler.pkl')
    with open(MODELS_DIR / 'feature_info.json', 'r') as f:
        feature_info = json.load(f)
    return model, scaler, feature_info['feature_columns']

def get_latest_activity_data() -> tuple:
    """Get TRUE latest activity - sorted by Date DESC."""
    if not ACTIVITIES_CSV.exists():
        raise FileNotFoundError(f"{ACTIVITIES_CSV} not found. Run Phase 1!")
    
    # ✅ LOAD + SORT BY DATE (fixes "first run" issue)
    df = pd.read_csv(ACTIVITIES_CSV)
    if df.empty:
        raise ValueError("No activities found")
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.sort_values('Date', ascending=False).reset_index(drop=True)
    
    latest = df.iloc[0]  # ✅ Now TRUE latest!
    print(f"📊 Predicting LATEST run: {latest.get('Date', 'Unknown')} | {latest.get('Distance', 0):.1f}km")
    
    return df, latest

def predict_new_run(df: pd.DataFrame, latest_row: pd.Series, model, scaler, feature_cols: list) -> dict:
    """Predict form score + gaps."""
    # ✅ SAFE PARSING with pace fix
    profile = {
        'avgcadence': safe_float(latest_row.get('Avg Run Cadence', 160)),
        'avgverticaloscillation': safe_float(latest_row.get('Avg Vertical Oscillation', 8.0)),
        'avggroundcontacttime': safe_float(latest_row.get('Avg Ground Contact Time', 260)),
        'avgstepspeedlosspct': safe_float(latest_row.get('Avg Step Speed Loss %', 5.5)),
        'avghr': safe_float(latest_row.get('Avg HR', 155)),
        'avgpaceminkm': parse_garmin_pace(latest_row.get('Avg Pace', '5:30'))  # ✅ Fixed!
    }
    
    features = np.array([
        profile['avgcadence'], profile['avgverticaloscillation'],
        profile['avggroundcontacttime'], profile['avgstepspeedlosspct'],
        profile['avghr'], profile['avgpaceminkm']
    ])
    
    # Predict
    features_scaled = scaler.transform(features.reshape(1, -1))
    form_score = model.predict(features_scaled)[0]
    
    # Elite gaps
    # In predict_new_run(), elite_targets:
    elite_targets = {
        'cadencespm': 175,
        'verticaloscillationcm': 7.2, 
        'groundcontacttimems': 245,
        'stepspeedlosspct': 4.5,
        'paceminkm': 5.15  # ✅ Elite 50yo marathon pace
    }

    
    gaps = {}
    col_map = ['cadencespm', 'verticaloscillationcm', 'groundcontacttimems', 
               'stepspeedlosspct', 'paceminkm']
    for i, col in enumerate(col_map):
        gaps[col] = {
            'current': features[i],
            'target': elite_targets[col],
            'gap': features[i] - elite_targets[col]
        }
    
    return {
        'form_score': round(form_score, 1),
        'profile': profile,
        'gaps': gaps,
        'priority_gaps': sorted(gaps.items(), key=lambda x: abs(x[1]['gap']), reverse=True)[:3],
        'activity_date': str(latest_row.get('Date', 'Unknown'))
    }

def safe_float(value):
    """Safe float conversion."""
    try:
        return float(value) if value is not None else 0.0
    except Exception:
        return 0.0

if __name__ == "__main__":
    print("🎯 PHASE 5: FORM PREDICTION")
    model, scaler, feature_cols = load_model_components()
    
    try:
        df, latest = get_latest_activity_data()
        results = predict_new_run(df, latest, model, scaler, feature_cols)
        
        print(f"\n🏆 FORM SCORE: {results['form_score']}/100")
        print(f"📅 {results['activity_date']}")
        
        print("\n🔥 TOP 3 GAPS:")
        for i, (metric, gap) in enumerate(results['priority_gaps'], 1):
            metric_name = metric.replace('stepspeedlosspct', 'SSL').replace('paceminkm', 'Pace')
            print(f"  {i}. {metric_name}: {gap['current']:.1f} → {gap['target']:.1f} "
                  f"(gap {gap['gap']:+.1f})")
        
        # Save
        with open(DATA_DIR / "prediction_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Saved: {DATA_DIR}/prediction_results.json")
        
    except Exception as e:
        print(f"❌ {e}")
        print("Run: ./run.sh")
