#!/usr/bin/env python3
import sys
import traceback
from pathlib import Path

# Fix imports
sys.path.insert(0, str(Path(__file__).parent / 'src/garmin_ai'))

def test_imports():
    print("🔍 Testing imports...")
    try:
        from activities_analyzer import analyze_activities, load_activities
        print("✅ Phase 1 imports OK")
    except Exception as e:
        print(f"❌ Phase 1 import failed: {e}")
        traceback.print_exc()
        return False
    
    try:
        from form_analyzer import load_data
        print("✅ Phase 2 imports OK")
    except Exception as e:
        print(f"❌ Phase 2 import failed: {e}")
    
    try:
        from synthetic_data_generator import load_current_profile
        print("✅ Phase 3 imports OK")
    except Exception as e:
        print(f"❌ Phase 3 import failed: {e}")
    
    return True

def phase1():
    print("\n📥 PHASE 1: DATA INGESTION")
    try:
        from activities_analyzer import (
            analyze_activities,
            create_running_profile,
            load_activities,
            print_analysis,
            save_running_profile,
        )
        df = load_activities()
        print(f"📊 Loaded {len(df)} activities")
        if df.empty:
            print("❌ No data - copy Activities.csv to data/")
            return False
        
        analysis = analyze_activities(df)
        print_analysis(analysis)
        profile = create_running_profile(analysis)
        save_running_profile(profile)
        print("✅ Phase 1 COMPLETE")
        return True
    except Exception as e:
        print(f"❌ Phase 1 FAILED: {e}")
        traceback.print_exc()
        return False

def main():
    print("🚀 GARMIN RUNNING AI PIPELINE")
    print("=" * 60)
    
    if not test_imports():
        print("❌ Import errors - check PYTHONPATH")
        return
    
    phase1()
    
    print("\n🎉 DEBUG COMPLETE - Check where it stops!")

if __name__ == "__main__":
    main()