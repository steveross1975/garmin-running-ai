# train_model.py - FIXED: Column name mismatch (snake_case vs camelCase)
import json

import joblib
import numpy as np
import pandas as pd
from config import MODELS_DIR, SYNTHETIC_ALL_PROFILES_CSV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

MODELS_DIR.mkdir(parents=True, exist_ok=True)

def load_training_data() -> pd.DataFrame:
    """Load master synthetic dataset."""
    if not SYNTHETIC_ALL_PROFILES_CSV.exists():
        raise FileNotFoundError(f"Synthetic data not found: {SYNTHETIC_ALL_PROFILES_CSV}")
    
    df = pd.read_csv(SYNTHETIC_ALL_PROFILES_CSV)
    print(f"✅ Loaded {len(df)} synthetic runs")
    print("📊 Columns:", list(df.columns))
    return df

# fix_column_names() - BULLETPROOF VERSION
def fix_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Convert snake_case → camelCase + ensure ALL features exist."""
    print(f"🔍 Input columns: {list(df.columns)}")
    
    # Step 1: Rename existing columns
    column_mapping = {
        'cadence_spm': 'cadencespm',
        'vertical_oscillation_cm': 'verticaloscillationcm',
        'ground_contact_time_ms': 'groundcontacttimems',
        'step_speed_loss_pct': 'stepspeedlosspct',
        'pace_min_km': 'paceminkm',
        'heart_rate_bpm': 'heartratebpm'  # If exists
    }
    
    df = df.rename(columns=column_mapping).copy()
    print(f"📝 After rename: {list(df.columns)[:10]}...")
    
    # Step 2: Ensure ALL 6 required features exist (fill/create as needed)
    feature_cols = ['cadencespm', 'verticaloscillationcm', 'groundcontacttimems', 
                   'stepspeedlosspct', 'heartratebpm', 'paceminkm']
    
    for col in feature_cols:
        if col not in df.columns:
            print(f"⚠️  Creating missing column: {col}")
            
            if col == 'cadencespm':
                df[col] = 170.0  # Elite default
            elif col == 'verticaloscillationcm':
                df[col] = 7.5
            elif col == 'groundcontacttimems':
                df[col] = 255.0
            elif col == 'stepspeedlosspct':
                df[col] = 5.0
            elif col == 'paceminkm':
                # Derive from existing distance/duration if possible
                if 'distance_km' in df.columns and 'duration_min' in df.columns:
                    df[col] = df['duration_min'] / df['distance_km']
                else:
                    df[col] = 5.30  # Elite pace
            elif col == 'heartratebpm':
                # Smart generation from cadence + pace
                cadence_mean = df.get('cadencespm', 170)
                pace_mean = df.get('paceminkm', 5.3)
                df[col] = 160 + (pace_mean - 5.0) * 20 - (cadence_mean - 170) * 0.3
                df[col] = df[col].clip(140, 180)
    
    # Step 3: Fill any NaNs with means
    for col in feature_cols:
        df[col] = df[col].fillna(df[col].mean())
    
    print(f"✅ ALL features ready: {feature_cols}")
    print(f"   Ranges: cadence={df['cadencespm'].min():.0f}-{df['cadencespm'].max():.0f}")
    return df


# FIXED: prepare_features_target() - Broadcast error fix
def prepare_features_target(df: pd.DataFrame) -> tuple:
    """Prepare ML-ready features and targets - FIXED broadcast error."""
    df = fix_column_names(df)
    
    feature_cols = [
        'cadencespm', 'verticaloscillationcm', 'groundcontacttimems', 
        'stepspeedlosspct', 'heartratebpm', 'paceminkm'
    ]
    
    # Elite targets (repeat for all rows)
    elite_targets_dict = {
        'cadencespm': 175.0,
        'verticaloscillationcm': 7.2,
        'groundcontacttimems': 245.0,
        'stepspeedlosspct': 4.5,
        'paceminkm': 5.15
    }
    
    # HR efficiency (not in form score)
    df['hrefficiency'] = 170.0 / df['heartratebpm'].clip(1) * 100
    df['hrefficiency'] = df['hrefficiency'].clip(0, 100)
    
    # Calculate per-row errors (FIXED: broadcast across all rows)
    form_errors = np.zeros(len(df))
    weights = [0.20, 0.25, 0.25, 0.20, 0.10]  # cadencespm, vo, gct, ssl, pace
    
    for i, col in enumerate(['cadencespm', 'verticaloscillationcm', 'groundcontacttimems', 
                           'stepspeedlosspct', 'paceminkm']):
        target = elite_targets_dict[col]
        error = np.abs(df[col] - target) / target
        form_errors += error * weights[i]
    
    df['form_score'] = np.clip((1.0 - form_errors) * 100, 0, 100)
    
    # Features matrix
    X = df[feature_cols].values
    y = df['form_score'].values
    
    print(f"✅ Features: {X.shape}, Form scores: {y.min():.1f}-{y.max():.1f}")
    print(f"   Sample: {X[0].round(1)} → score {y[0]:.1f}")
    
    return X, y, feature_cols

def train_model(X: np.ndarray, y: np.ndarray, feature_cols: list):
    """Train RandomForestRegressor."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train_s, y_train)
    
    # Results
    train_score = r2_score(y_train, model.predict(X_train_s))
    test_score = r2_score(y_test, model.predict(X_test_s))
    test_rmse = np.sqrt(mean_squared_error(y_test, model.predict(X_test_s)))
    
    print(f"📈 Train R²: {train_score:.3f} | Test R²: {test_score:.3f} | RMSE: {test_rmse:.1f}")
    print(f"🎯 Feature Importances: {dict(zip(feature_cols, model.feature_importances_.round(3)))}")
    
    return model, scaler, feature_cols

def save_model(model, scaler, feature_cols):
    """Persist trained model."""
    joblib.dump(model, MODELS_DIR / 'form_predictor_model.pkl')
    joblib.dump(scaler, MODELS_DIR / 'feature_scaler.pkl')
    
    with open(MODELS_DIR / 'feature_info.json', 'w') as f:
        json.dump({'feature_columns': feature_cols}, f, indent=2)
    
    print(f"💾 Model saved: {MODELS_DIR.absolute()}")

if __name__ == "__main__":
    print("🚀 GARMIN RUNNING AI - PHASE 5: ML TRAINING")
    print("=" * 60)
    
    df = load_training_data()
    X, y, feature_cols = prepare_features_target(df)
    model, scaler, feature_cols = train_model(X, y, feature_cols)
    save_model(model, scaler, feature_cols)
    
    print("\n✅ PHASE 5 SUCCESS! Model ready for .fit prediction 🏃‍♂️")
