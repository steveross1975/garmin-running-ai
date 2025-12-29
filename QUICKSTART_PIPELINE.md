# 🚀 UNIFIED PIPELINE ORCHESTRATOR - QUICK START GUIDE

## One Command to Rule Them All

Instead of running multiple modules separately, you can now execute the **entire pipeline** with a single command:

```bash
./run.sh
```

That's it! This automatically runs:
- **Phase 1**: Data Ingestion (FIT → CSV → Summary)
- **Phase 2**: Data Analysis (Form → Profiles → Synthetic Data)
- **Phase 3**: ML Models (coming soon)
- **Phase 4**: AI Tips (coming soon)

---

## 🎯 How to Use

### Setup (One Time)
```bash
# Make the script executable
chmod +x run.sh

# Ensure virtual environment is created
python -m venv .venv

# Install dependencies
pip install -r requirements.txt
```

### Run (Every Time)
```bash
# Option 1: Full pipeline (recommended)
./run.sh

# Option 2: Direct Python
source .venv/bin/activate
python pipeline.py
```

---

## 📋 Available Commands

### Run All Phases
```bash
./run.sh
```

### Run Specific Phases
```bash
# Just Phase 1 (data ingestion)
./run.sh --phase 1

# Just Phase 2 (data analysis)
./run.sh --phase 2

# Phases 1 and 2
./run.sh --phase 1,2
```

### Skip Phases
```bash
# Everything except Phase 3
./run.sh --skip-phase 3

# Everything except Phases 3 and 4
./run.sh --skip-phase 3,4
```

### Preview Without Running
```bash
# See what will happen without executing
./run.sh --dry-run

# Preview just Phase 2
./run.sh --phase 2 --dry-run
```

---

## ⏱️ Execution Times

| Scenario | Time |
|----------|------|
| Full pipeline (Phases 1-2) | ~45-60 seconds |
| Phase 1 only (FIT conversion) | ~15-30 seconds |
| Phase 2 only (analysis) | ~20-30 seconds |
| Dry run (no execution) | ~2-3 seconds |

---

## 📁 What Gets Generated

```
data/
├── Activities.csv                          ← Master activity summary
├── running_profile.json                    ← Your baseline metrics
├── form_analysis.json                      ← Your form score (78.5/100)
├── target_profiles.json                    ← 3 improvement profiles
└── synthetic/
    ├── synthetic_steady_runner.csv         ← 144 training runs
    ├── synthetic_efficient_runner.csv      ← 144 training runs
    ├── synthetic_balanced_runner.csv       ← 144 training runs
    └── synthetic_all_profiles.csv          ← 432 combined

logs/
└── pipeline.log                            ← Detailed execution log
```

---

## 🔍 Monitor Progress

### Real-Time Console Output
As the pipeline runs, you'll see:
```
╔════════════════════════════════════════════════════════════════════════════════╗
║           🏃 GARMIN RUNNING AI - UNIFIED PIPELINE ORCHESTRATOR 🏃            ║
╚════════════════════════════════════════════════════════════════════════════════╝

✅ All dependencies ready

▶ ════════════════════════════════════════════════════════════════════════════════
▶ PHASE 1: Data Ingestion & Foundation [START]
▶ ════════════════════════════════════════════════════════════════════════════════

2025-12-29 22:50:45 - pipeline - INFO - Starting Phase 1: Data Ingestion
2025-12-29 22:50:45 - pipeline - INFO - Found 3 FIT files
2025-12-29 22:50:46 - pipeline - INFO - Converting FIT files to CSV...
2025-12-29 22:50:48 - pipeline - INFO - Analyzing activities...
✅ Phase 1 complete: Data ingested and analyzed

▶ ════════════════════════════════════════════════════════════════════════════════
▶ PHASE 2: Data Analysis & Baselines [START]
▶ ════════════════════════════════════════════════════════════════════════════════

2025-12-29 22:50:48 - pipeline - INFO - Starting Phase 2: Data Analysis
2025-12-29 22:50:49 - pipeline - INFO - Step 2.1: Analyzing running form...
📊 RUNNING FORM ANALYSIS REPORT
🎯 OVERALL FORM SCORE: 78.5/100 ✅ GOOD
...
✅ Phase 2 complete: Form analysis, profiles, synthetic data ready

╔════════════════════════════════════════════════════════════════════════════════╗
║                         PIPELINE EXECUTION SUMMARY                            ║
╚════════════════════════════════════════════════════════════════════════════════╝

✅ Phase 1: Data Ingestion & Foundation
✅ Phase 2: Data Analysis & Baselines
⏸️  Phase 3: Machine Learning Models
⏸️  Phase 4: Generative AI Tips

⏱️  Total time: 52.4s

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

### Check the Log
```bash
# View last 50 lines
tail -50 data/pipeline.log

# Follow live (if running)
tail -f data/pipeline.log
```

---

## 🎯 Common Workflows

### Workflow 1: New Garmin Data Arrives
```bash
# 1. Copy new FIT files to data/fit/
cp ~/Downloads/*.fit data/fit/

# 2. Run full pipeline
./run.sh

# 3. Review results
cat data/form_analysis.json | jq .
```

### Workflow 2: Just Update Analysis
```bash
# Skip FIT conversion, update analysis only
./run.sh --phase 2
```

### Workflow 3: Prepare for ML Training
```bash
# Ensure Phases 1-2 are complete and synthetic data is ready
./run.sh --phase 1,2

# Verify synthetic data exists
ls -lh data/synthetic/synthetic_all_profiles.csv
```

### Workflow 4: Dry Run Before Committing
```bash
# See what will happen
./run.sh --dry-run

# If satisfied, run for real
./run.sh
```

---

## 🔧 Troubleshooting

### Problem: "Permission denied" on run.sh
```bash
chmod +x run.sh
./run.sh
```

### Problem: "Virtual environment not found"
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
./run.sh
```

### Problem: "No FIT files found"
```bash
# Add your FIT files to the directory
mkdir -p data/fit
cp /path/to/your/*.fit data/fit/
./run.sh
```

### Problem: Pipeline hangs or fails
```bash
# Check the log
tail -100 data/pipeline.log

# Run specific phase with verbose output
python pipeline.py --phase 2 --verbose
```

---

## 💾 Commit to GitHub

After first successful run:
```bash
git add pipeline.py run.sh PIPELINE.md data/Activities.csv data/form_analysis.json
git commit -m "Add unified pipeline orchestrator - run all phases with single command"
git push
```

---

## 🚀 What's Next?

After running the pipeline successfully:

1. ✅ **Review Results**
   ```bash
   cat data/form_analysis.json | jq .overall_score
   ```

2. ✅ **Check Synthetic Data**
   ```bash
   wc -l data/synthetic/synthetic_all_profiles.csv
   head -5 data/synthetic/synthetic_all_profiles.csv
   ```

3. ✅ **Prepare for Phase 3 (ML)**
   - Pipeline is ready for ML model training
   - Have 432 synthetic runs for training
   - All metrics prepared

---

## 📖 Full Documentation

For detailed information about each phase, see:
- **PHASES_1_2_RECAP.md** - Complete breakdown of Phases 1 & 2
- **PIPELINE.md** - Extended pipeline documentation
- **Phase 2 modules** - `form_analyzer.py`, `target_profiles.py`, `synthetic_data_generator.py`

---

## 🎉 You're Done!

Your AI running pipeline is now:
- ✅ **Automated** - Run all phases with one command
- ✅ **Reproducible** - Same results every time
- ✅ **Logged** - Full execution details saved
- ✅ **Professional** - Production-ready code
- ✅ **Ready for ML** - 432 synthetic runs generated

**Now you can focus on the science, not the tooling!** 🏃‍♂️
