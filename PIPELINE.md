# Unified Pipeline Orchestrator - Complete Guide

## 🎯 Overview

The **Pipeline Orchestrator** is a single entry point that runs all phases automatically:

```
ONE COMMAND → Phase 1 → Phase 2 → Phase 3 → Phase 4 → COMPLETE ✅
```

Instead of running:
```bash
python -m src.garmin_ai.fit_converter
python -m src.garmin_ai.activities_analyzer
python -m src.garmin_ai.form_analyzer
python -m src.garmin_ai.target_profiles
python -m src.garmin_ai.synthetic_data_generator
```

You now run:
```bash
python pipeline.py
```

---

## 🚀 Quick Start

### Option 1: Using the Bash Script (Recommended for macOS/Linux)

```bash
chmod +x run.sh
./run.sh
```

This automatically:
- Activates virtual environment
- Verifies dependencies
- Runs the full pipeline
- Displays results

### Option 2: Using Python Directly

```bash
source .venv/bin/activate
python pipeline.py
```

---

## 📋 Commands & Options

### Run All Phases
```bash
python pipeline.py
```
Executes: Phase 1 → Phase 2 → Phase 3 → Phase 4

### Run Specific Phases
```bash
# Run only Phase 1 (Data Ingestion)
python pipeline.py --phase 1

# Run only Phase 2 (Data Analysis)
python pipeline.py --phase 2

# Run Phases 1 and 2
python pipeline.py --phase 1,2

# Run Phases 2, 3, and 4
python pipeline.py --phase 2,3,4
```

### Skip Phases
```bash
# Run all except Phase 3
python pipeline.py --skip-phase 3

# Run all except Phases 3 and 4
python pipeline.py --skip-phase 3,4
```

### Dry Run (Preview Without Executing)
```bash
# See what will run without actually running it
python pipeline.py --dry-run

# Preview phases 1 and 2 only
python pipeline.py --phase 1,2 --dry-run
```

### Verbose Output
```bash
python pipeline.py --verbose
```

---

## 📊 Pipeline Structure

```
┌─────────────────────────────────────────────────────────────┐
│          PHASE 1: DATA INGESTION & FOUNDATION              │
├─────────────────────────────────────────────────────────────┤
│ 1.1 Check FIT files in data/fit/                           │
│ 1.2 Convert FIT → CSV (per-second data)                    │
│ 1.3 Analyze all activities                                  │
│ ↓ Output: Activities.csv, running_profile.json             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│        PHASE 2: DATA ANALYSIS & BASELINES                  │
├─────────────────────────────────────────────────────────────┤
│ 2.1 Form Analysis (score your form 0-100)                  │
│ 2.2 Target Profiles (define 3 runner archetypes)           │
│ 2.3 Synthetic Data (generate 432 training runs)            │
│ ↓ Output: form_analysis.json, target_profiles.json,        │
│           synthetic_*.csv (432 runs)                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│      PHASE 3: MACHINE LEARNING MODELS                      │
├─────────────────────────────────────────────────────────────┤
│ 3.1 Form Efficiency Predictor (LSTM) - TBD               │
│ 3.2 Running Dynamics Approximator (Regression) - TBD     │
│ 3.3 Zone Optimizer (Clustering) - TBD                    │
│ ↓ Output: models/*.pkl, models/*.h5                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│      PHASE 4: GENERATIVE AI TIPS                           │
├─────────────────────────────────────────────────────────────┤
│ 4.1 Load your current metrics                              │
│ 4.2 Predict form score + running dynamics                  │
│ 4.3 Generate personalized tips - TBD                     │
│ ↓ Output: form_tips.json, coaching_report.md              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Input & Output Files

### Input Requirements
```
data/
├── fit/
│   ├── 21328723558.fit ← Your Garmin FIT files
│   ├── 21328723559.fit
│   └── 21328723560.fit
```

If you provide FIT files, Phase 1 will automatically:
- Convert to CSV
- Extract Activities summary
- Build running profile

### Phase 1 Outputs
```
data/
├── csv/
│   ├── 21328723558.csv ← Converted time-series
│   ├── 21328723559.csv
│   └── 21328723560.csv
├── Activities.csv ← Master summary (3 activities)
└── running_profile.json ← Your baseline metrics
```

### Phase 2 Outputs
```
data/
├── form_analysis.json ← Your form scores (78.5/100)
├── target_profiles.json ← 3 goal profiles
└── synthetic/
    ├── synthetic_steady_runner.csv ← 144 runs
    ├── synthetic_efficient_runner.csv ← 144 runs
    ├── synthetic_balanced_runner.csv ← 144 runs
    └── synthetic_all_profiles.csv ← 432 combined
```

### Phase 3 Outputs (Coming)
```
models/
├── form_efficiency_model.h5 ← LSTM model
├── dynamics_approximator.pkl ← Regression model
└── zone_optimizer.pkl ← Clustering model
```

### Phase 4 Outputs (Coming)
```
data/
├── form_tips.json ← AI-generated tips
└── coaching_report.md ← Personalized coaching
```

---

## 🔍 Monitoring & Logging

### View Real-Time Output
All phases print progress to console:
```
▶ ════════════════════════════════════════════════════════════════════════════════
▶ PHASE 1: Data Ingestion & Foundation [START]
▶ ════════════════════════════════════════════════════════════════════════════════

2025-12-29 22:50:45 - pipeline - INFO - Starting Phase 1: Data Ingestion
2025-12-29 22:50:45 - pipeline - INFO - Found 3 FIT files
2025-12-29 22:50:46 - pipeline - INFO - Converting FIT files to CSV...
2025-12-29 22:50:46 - pipeline - INFO -   Converting: 21328723558.fit
...
✅ Phase 1 complete: Data ingested and analyzed
```

### Check Pipeline Log
```bash
tail -f data/pipeline.log
```

### Summary Output
After each run:
```
╔════════════════════════════════════════════════════════════════════════════════╗
║                         PIPELINE EXECUTION SUMMARY                            ║
╚════════════════════════════════════════════════════════════════════════════════╝

✅ Phase 1: Data Ingestion & Foundation
✅ Phase 2: Data Analysis & Baselines
⏸️  Phase 3: Machine Learning Models
⏸️  Phase 4: Generative AI Tips

⏱️  Total time: 45.3s

📊 Output directory: data/

📁 Generated files:

  Analysis:
    - form_analysis.json (1,250 bytes)
    - target_profiles.json (2,847 bytes)

  Data:
    - Activities.csv (1,542 bytes)
    - running_profile.json (856 bytes)

  Synthetic:
    - synthetic_balanced_runner.csv (45.2 KB)
    - synthetic_efficient_runner.csv (45.1 KB)
    - synthetic_steady_runner.csv (45.3 KB)
    - synthetic_all_profiles.csv (135.6 KB)
```

---

## 🎯 Common Workflows

### Workflow 1: Fresh Run (New FIT Files)
```bash
# Put new FIT files in data/fit/
cp ~/Downloads/*.fit data/fit/

# Run full pipeline
./run.sh
```

This will:
- Convert new FIT files to CSV
- Update Activities.csv
- Recalculate form analysis
- Regenerate target profiles
- Create new synthetic data

**Time**: ~45-60 seconds

---

### Workflow 2: Just Analyze Existing Data
```bash
./run.sh --phase 2
```

Skips FIT conversion, runs form analysis only.

**Time**: ~15-20 seconds

---

### Workflow 3: Regenerate Synthetic Data
```bash
./run.sh --phase 2 --dry-run  # Preview
./run.sh --phase 2             # Execute
```

Regenerates 432 training examples based on latest analysis.

**Time**: ~20-30 seconds

---

### Workflow 4: Prepare for ML Training
```bash
./run.sh --phase 1,2
```

Ensures data is ready for Phase 3 ML models.

**Time**: ~30-45 seconds

---

### Workflow 5: Preview Before Running
```bash
./run.sh --dry-run
```

Shows exactly what will happen without executing.

---

## 🔧 Troubleshooting

### Issue: "No FIT files found"
**Cause**: No `.fit` files in `data/fit/`

**Solution**:
```bash
# Copy your Garmin FIT files to data/fit/
cp /path/to/your/*.fit data/fit/

# Run pipeline
./run.sh
```

### Issue: Missing Dependencies
**Error**: `ImportError: No module named 'fitparse'`

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: Permission Denied on run.sh
**Error**: `bash: ./run.sh: Permission denied`

**Solution**:
```bash
chmod +x run.sh
./run.sh
```

### Issue: Virtual Environment Not Activated
**Error**: `python: command not found` or wrong Python version

**Solution**:
```bash
# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run pipeline
./run.sh
```

### Issue: Pipeline Stops Mid-Execution
**Cause**: Likely an error in a specific phase

**Solution**:
```bash
# Check the log
tail -100 data/pipeline.log

# Run just that phase
./run.sh --phase 2 --verbose

# Check what files are missing
ls -la data/
```

---

## 📈 Performance Notes

### Phase Execution Times
| Phase | Time | Condition |
|-------|------|-----------|
| **Phase 1** | 15-30s | With 3 FIT files |
| **Phase 2** | 20-30s | Form analysis + synthetic (432 runs) |
| **Phase 3** | TBD | Not implemented yet |
| **Phase 4** | TBD | Not implemented yet |
| **Total (1+2)** | 45-60s | Full fresh run |

### Tips for Faster Execution
1. Skip phases you don't need: `./run.sh --phase 1,2`
2. Run only Phase 2 if FIT files haven't changed: `./run.sh --phase 2`
3. Use dry-run to preview: `./run.sh --dry-run`

---

## 🚀 Next Steps

### After First Run
1. ✅ Check `data/form_analysis.json` for your form score
2. ✅ Review `data/target_profiles.json` for improvement goals
3. ✅ Inspect `data/synthetic/` for training data
4. ✅ Commit to GitHub: `git add -A && git commit -m "Pipeline complete"`

### To Prepare for ML (Phase 3)
1. ✅ Verify `data/synthetic/synthetic_all_profiles.csv` exists (432 rows)
2. ✅ Check that all 15 metrics are present (cadence, VO, GCT, SSL, HR, etc.)
3. ✅ Ready to train models!

### To Add Custom Phases
Edit `pipeline.py`:
```python
def run_phase_5_custom(self):
    """Your custom phase."""
    if 5 not in self.phases:
        return
    
    self.log_section(5)
    logger.info("Running custom phase...")
    
    # Your code here
    
    self.results[5] = {"status": "success"}
```

Then run:
```bash
python pipeline.py --phase 5
```

---

## 📊 Architecture Details

### How the Orchestrator Works

1. **Parse Arguments**: Read command-line options
2. **Initialize**: Set up logging and directories
3. **Execute Phases**: Run selected phases in sequence
4. **Handle Dependencies**: Auto-run Phase 1 if needed by Phase 2
5. **Log Results**: Track status of each phase
6. **Print Summary**: Show what was created

### Module Dependencies
```
pipeline.py (orchestrator)
    ↓
    ├→ Phase 1: garmin_client.py → fit_converter.py → activities_analyzer.py
    │
    ├→ Phase 2: form_analyzer.py → target_profiles.py → synthetic_data_generator.py
    │
    ├→ Phase 3: (to be implemented)
    │
    └→ Phase 4: (to be implemented)
```

---

## 💡 Advanced Usage

### Automated Nightly Runs
```bash
# Add to crontab for daily 2 AM execution
0 2 * * * cd /path/to/garmin-running-ai && ./run.sh >> logs/daily.log 2>&1
```

### CI/CD Integration
```yaml
# GitHub Actions example
name: Pipeline
on: [push]
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python pipeline.py --phase 1,2
```

### Docker Containerization
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "pipeline.py"]
```

---

## 🎉 Summary

**Before**: Run 5 commands manually  
**After**: Single `./run.sh` command

✅ Reproducible  
✅ Automated  
✅ Logged  
✅ Extensible  
✅ Professional  

**Your data pipeline is now production-ready!** 🚀
