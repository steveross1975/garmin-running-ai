#!/bin/bash
set -e

RED='\033[0;31m' GREEN='\033[0;32m' BLUE='\033[0;34m' NC='\033[0m'
SRC_DIR="$(dirname "$(realpath "$0")")/src/garmin_ai"

print_banner() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║ 🚀 GARMIN RUNNING AI PIPELINE${NC}${BLUE}║"
    echo "║ Forerunner 970 + HRM-600 → Elite Form → ML Training Data                    ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
}

print_banner
cd "$SRC_DIR" && export PYTHONPATH=.

echo "📥 1/4: Analysis"
python3 activities_analyzer.py

echo "📊 2/4: Form Analysis"
python3 form_analyzer.py

echo "🎯 3/4: Target Profiles ← FIXED SAVE!"
python3 target_profiles.py

echo "🔬 4/4: Synthetic Data (432 ML runs)"
python3 synthetic_data_generator.py

echo "Phase 5: ML Training"
python models/train_model.py

echo "Phase 5: Test Prediction"
python models/predict_form_gaps.py

echo "Phase 5: Generate AI Tips"  
python models/generate_ai_tips.py

echo -e "${GREEN}🎉 PIPELINE COMPLETE!${NC}"