#!/bin/bash
# Quick execution script for the unified pipeline

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                                ║"
echo "║           🏃 GARMIN RUNNING AI - UNIFIED PIPELINE ORCHESTRATOR 🏃             ║"
echo "║                                                                                ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Activate virtual environment
if [ -d ".running_ai" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source .running_ai/bin/activate
else
    echo -e "${RED}❌ Virtual environment not found. Run: python -m venv .venv${NC}"
    exit 1
fi

# Check if Python modules can be imported
echo -e "${YELLOW}Verifying dependencies...${NC}"
python -c "import fitparse, pandas, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Missing dependencies. Run: pip install -r requirements.txt${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All dependencies ready${NC}"
echo ""

# Parse command-line arguments
PHASE=""
SKIP_PHASE=""
DRY_RUN=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --phase)
            PHASE="--phase $2"
            shift 2
            ;;
        --skip-phase)
            SKIP_PHASE="--skip-phase $2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN="--dry-run"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo ""
            echo "Usage: ./run.sh [options]"
            echo ""
            echo "Options:"
            echo "  --phase NUM         Run specific phases (e.g., --phase 1,2)"
            echo "  --skip-phase NUM    Skip specific phases (e.g., --skip-phase 3)"
            echo "  --dry-run           Show plan without executing"
            echo ""
            echo "Examples:"
            echo "  ./run.sh                           # Run all phases"
            echo "  ./run.sh --phase 1,2               # Run phases 1 and 2"
            echo "  ./run.sh --skip-phase 3,4          # Run all except phases 3 and 4"
            echo "  ./run.sh --dry-run                 # Show what would run"
            exit 0
            ;;
    esac
done

# Run pipeline
echo -e "${BLUE}Executing pipeline...${NC}"
echo ""

python pipeline.py $PHASE $SKIP_PHASE $DRY_RUN

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Pipeline completed successfully${NC}"
    echo ""
    echo -e "${BLUE}📊 Check results:${NC}"
    echo "  • Form analysis: data/form_analysis.json"
    echo "  • Target profiles: data/target_profiles.json"
    echo "  • Synthetic data: data/synthetic/"
    echo "  • Pipeline log: data/pipeline.log"
else
    echo -e "${RED}❌ Pipeline failed (exit code: $EXIT_CODE)${NC}"
    echo "Check data/pipeline.log for details"
fi

exit $EXIT_CODE
