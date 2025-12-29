# 🎯 PIPELINE CHEAT SHEET - Quick Reference

## ONE COMMAND TO RULE THEM ALL

```bash
./run.sh
```

---

## 📋 COMMANDS AT A GLANCE

| Command | What It Does |
|---------|--------------|
| `./run.sh` | Run all 4 phases |
| `./run.sh --phase 1` | Run only Phase 1 (FIT conversion) |
| `./run.sh --phase 2` | Run only Phase 2 (analysis) |
| `./run.sh --phase 1,2` | Run phases 1 and 2 |
| `./run.sh --skip-phase 3` | Run all except Phase 3 |
| `./run.sh --dry-run` | Preview without executing |
| `./run.sh --verbose` | Detailed output |
| `python pipeline.py` | Direct Python execution |

---

## ⏱️ EXECUTION TIMES

- **Full pipeline**: ~60 seconds
- **Phase 1 only**: ~15-30 seconds
- **Phase 2 only**: ~20-30 seconds
- **Dry-run**: ~2-3 seconds

---

## 📁 KEY FILES GENERATED

After running:
```
data/
├── form_analysis.json          ← Your form score (78.5/100) ⭐
├── target_profiles.json        ← Improvement goals
├── Activities.csv              ← Master summary
└── synthetic/
    └── synthetic_all_profiles.csv  ← 432 training runs
```

---

## 🔍 CHECK YOUR RESULTS

```bash
# View form score
cat data/form_analysis.json | jq .overall_score

# View detailed analysis
cat data/form_analysis.json | jq .

# Check synthetic data count
wc -l data/synthetic/synthetic_all_profiles.csv

# View log
tail -20 data/pipeline.log
```

---

## 🚨 COMMON ISSUES & FIXES

| Issue | Fix |
|-------|-----|
| `Permission denied: ./run.sh` | `chmod +x run.sh` |
| `No FIT files found` | `cp ~/Downloads/*.fit data/fit/` |
| `ModuleNotFoundError: fitparse` | `pip install -r requirements.txt` |
| `Pipeline hangs` | `./run.sh --phase 2` (skip FIT conversion) |
| `Missing Activities.csv` | Pipeline auto-fixes on next run |

---

## 💡 QUICK WORKFLOWS

### New Garmin Data
```bash
cp ~/Downloads/*.fit data/fit/
./run.sh
```

### Just Update Analysis
```bash
./run.sh --phase 2
```

### Preview Changes
```bash
./run.sh --phase 2 --dry-run
```

### Prepare for ML
```bash
./run.sh --phase 1,2
```

### Check Progress
```bash
tail -f data/pipeline.log
```

---

## 📊 WHAT EACH PHASE DOES

```
Phase 1: Data Ingestion
├─ Converts FIT files → CSV
├─ Extracts Activities.csv
└─ Builds running_profile.json

Phase 2: Data Analysis
├─ Scores your form (0-100)
├─ Defines target profiles
└─ Generates 432 synthetic runs

Phase 3: Machine Learning
└─ Coming soon...

Phase 4: Generative AI
└─ Coming soon...
```

---

## ✅ SETUP (ONE TIME)

```bash
chmod +x run.sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 RUN (EVERY TIME)

```bash
./run.sh
```

---

## 📚 DOCUMENTATION

- **USAGE_SUMMARY.md** ← You are here
- **QUICKSTART_PIPELINE.md** - Quick reference
- **PHASES_1_2_RECAP.md** - Technical details
- **PIPELINE.md** - Advanced usage

---

## 🎉 YOU'RE DONE!

Your pipeline is ready. Just add FIT files and run:

```bash
./run.sh
```

Check `data/form_analysis.json` for results. 📊
