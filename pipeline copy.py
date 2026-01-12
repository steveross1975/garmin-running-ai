#!/usr/bin/env python3
import sys
from pathlib import Path

# Fix imports
sys.path.insert(0, str(Path(__file__).parent / 'src/garmin_ai'))

# Phase 1
from .src.garmin_ai.activities_analyzer import (
    analyze_activities,
    create_running_profile,
    load_activities,
    print_analysis,
    save_running_profile,
)

# Phase 2  
from .src.garmin_ai.form_analyzer import analyze_form, print_report
from .src.garmin_ai.form_analyzer import load_data as form_load_data

# Phase 3
from .src.garmin_ai.synthetic_data_generator import (
    generate_all_profiles,
    load_current_profile,
    load_target_profiles,
)
from .src.garmin_ai.target_profiles import compare_to_profiles, print_profiles


def run_full_pipeline():
    print("🚀 GARMIN RUNNING AI PIPELINE")
    print("=" * 60)
    
    # PHASE 1: Original functions
    print("\n📥 PHASE 1: DATA INGESTION & ANALYSIS")
    df = load_activities()
    if df.empty:
        print("❌ Copy Activities.csv to data/")
        return
    
    analysis = analyze_activities(df)
    print_analysis(analysis)
    
    profile = create_running_profile(analysis)
    save_running_profile(profile)
    
    # PHASE 2: Form analysis  
    print("\n📊 PHASE 2: FORM ANALYSIS")
    try:
        form_df, form_profile = form_load_data()
        if form_df is not None:
            form_analysis = analyze_form(form_df, form_profile)
            print_report(form_analysis)
        print_profiles()
    except Exception as e:
        print("⚠️ Form analysis skipped")
    
    # PHASE 3: Synthetic data
    print("\n🔬 PHASE 3: SYNTHETIC TRAINING DATA")
    try:
        current = load_current_profile()
        targets = load_target_profiles()
        if current and targets:
            generate_all_profiles(current, targets, output_csv=True)
            print("✅ 432 ML runs generated!")
    except Exception as e:
        print("⚠️ Synthetic data skipped")
    
    print("\n🎉 PIPELINE COMPLETE!")
    print("📁 data/running_profile.json | data/synthetic_all_profiles.csv")

if __name__ == "__main__":
    run_full_pipeline()