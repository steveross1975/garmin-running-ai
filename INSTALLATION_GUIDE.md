# 📂 Installation Guide - Where to Place Files

## 🎯 Quick Answer

**Place these files in your project ROOT directory** (same level as `README.md`, `requirements.txt`):

```
garmin-running-ai/
├── pipeline.py         ← Copy here
├── run.sh              ← Copy here
├── USAGE_SUMMARY.md    ← Copy here
├── CHEAT_SHEET.md      ← Copy here
├── ... other files
```

---

## 📋 Step-by-Step Installation

### Step 1: Locate Your Project Root

Your project root is the top-level directory that contains:
```bash
ls -la ~/<path-to-project>/
# Should show:
# - README.md
# - requirements.txt
# - .gitignore
# - src/ (directory)
# - data/ (directory)
```

Example path: `/Users/yourname/Projects/garmin-running-ai/`

### Step 2: Copy `pipeline.py` to Root

```bash
# Navigate to your project root
cd /path/to/garmin-running-ai/

# You have the pipeline.py file from this session
# Copy it to the root directory
cp /path/to/downloaded/pipeline.py .

# Verify it's there
ls -la pipeline.py
# Output: -rw-r--r--  1 user  staff  13K Dec 29 22:50 pipeline.py
```

### Step 3: Copy `run.sh` to Root and Make Executable

```bash
# Copy the run.sh file
cp /path/to/downloaded/run.sh .

# Make it executable
chmod +x run.sh

# Verify
ls -la run.sh
# Output: -rwxr-xr-x  1 user  staff  2K Dec 29 22:50 run.sh
#         ↑ (x means executable)
```

### Step 4: Copy Documentation Files to Root

```bash
# Copy all documentation files
cp /path/to/USAGE_SUMMARY.md .
cp /path/to/CHEAT_SHEET.md .
cp /path/to/QUICKSTART_PIPELINE.md .
cp /path/to/PIPELINE.md .
cp /path/to/OPTIMIZATION_SUMMARY.md .

# Verify all are there
ls -la *.md
```

### Step 5: Verify Your Directory Structure

```bash
# From your project root, check that everything is in place
cd /path/to/garmin-running-ai/

# Should see these files in root:
ls -1 | grep -E "pipeline.py|run.sh|.*SUMMARY.md|CHEAT|PIPELINE"

# Output should be:
# CHEAT_SHEET.md
# OPTIMIZATION_SUMMARY.md
# PIPELINE.md
# QUICKSTART_PIPELINE.md
# USAGE_SUMMARY.md
# pipeline.py
# run.sh
```

---

## ✅ Complete File Placement Checklist

### Root Directory Files (Place Here ✅)

- [ ] `pipeline.py` - Main orchestrator
- [ ] `run.sh` - Bash launcher (executable)
- [ ] `USAGE_SUMMARY.md` - Usage guide
- [ ] `CHEAT_SHEET.md` - Quick reference
- [ ] `QUICKSTART_PIPELINE.md` - Quick start
- [ ] `PIPELINE.md` - Advanced guide
- [ ] `OPTIMIZATION_SUMMARY.md` - Before/after
- [ ] `PHASES_1_2_RECAP.md` - Technical details

### Already Existing in Root

- ✅ `README.md` - Your project readme
- ✅ `requirements.txt` - Python dependencies
- ✅ `.gitignore` - Git ignore rules
- ✅ `.env` - Environment variables
- ✅ `src/` - Source code directory
- ✅ `data/` - Data directory

### Generated During Pipeline Execution

These will be created automatically in `data/`:
- `Activities.csv`
- `running_profile.json`
- `form_analysis.json`
- `target_profiles.json`
- `pipeline.log`
- `csv/` - Converted FIT files
- `synthetic/` - Generated training data

---

## 🔍 Verify Installation

After copying all files, run this verification:

```bash
# From project root
cd /path/to/garmin-running-ai/

# Check that pipeline.py and run.sh exist
test -f pipeline.py && echo "✅ pipeline.py found" || echo "❌ pipeline.py missing"
test -f run.sh && echo "✅ run.sh found" || echo "❌ run.sh missing"

# Check that run.sh is executable
test -x run.sh && echo "✅ run.sh is executable" || echo "❌ run.sh not executable"

# Check documentation files
test -f USAGE_SUMMARY.md && echo "✅ USAGE_SUMMARY.md found" || echo "❌ missing"
test -f CHEAT_SHEET.md && echo "✅ CHEAT_SHEET.md found" || echo "❌ missing"

# Check source code directory
test -d src/garmin_ai && echo "✅ src/garmin_ai found" || echo "❌ missing"

# Check data directory
test -d data && echo "✅ data/ found" || echo "❌ missing"
```

Expected output:
```
✅ pipeline.py found
✅ run.sh found
✅ run.sh is executable
✅ USAGE_SUMMARY.md found
✅ CHEAT_SHEET.md found
✅ src/garmin_ai found
✅ data/ found
```

---

## 🚀 Test Installation

### Test 1: Check if run.sh is Executable
```bash
./run.sh --help
# Should show usage information
```

### Test 2: Check if pipeline.py Works
```bash
python pipeline.py --help
# Should show usage information
```

### Test 3: Run Dry-Run (Preview Only)
```bash
./run.sh --dry-run
# Should show what would happen without executing
```

### Test 4: View Documentation
```bash
# Any of these should work
cat CHEAT_SHEET.md
cat USAGE_SUMMARY.md | head -20
```

---

## 🎯 Final Setup

Once files are in place:

```bash
# 1. Create virtual environment (if not already done)
python -m venv .venv

# 2. Activate it
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Make run.sh executable (if not already done)
chmod +x run.sh

# 5. Verify everything works
./run.sh --dry-run
```

---

## 🔧 If You Have Trouble

### Error: "Permission denied: ./run.sh"
```bash
chmod +x run.sh
./run.sh
```

### Error: "pipeline.py: No such file or directory"
Make sure you're in the project root:
```bash
cd /path/to/garmin-running-ai/
pwd
# Should end with: .../garmin-running-ai

# Verify pipeline.py is here
ls -la pipeline.py
```

### Error: "No module named 'src.garmin_ai'"
Make sure you have:
1. `src/garmin_ai/` directory with modules
2. Virtual environment activated
3. Dependencies installed: `pip install -r requirements.txt`

### Error: "No FIT files found"
```bash
# Create fit directory if it doesn't exist
mkdir -p data/fit

# Copy your FIT files
cp ~/Downloads/*.fit data/fit/

# Run pipeline
./run.sh
```

---

## 📂 Complete Directory Structure After Setup

```
garmin-running-ai/
├── pipeline.py                      ✅ Copied
├── run.sh                           ✅ Copied (executable)
├── README.md
├── USAGE_SUMMARY.md                 ✅ Copied
├── CHEAT_SHEET.md                   ✅ Copied
├── QUICKSTART_PIPELINE.md           ✅ Copied
├── PIPELINE.md                      ✅ Copied
├── OPTIMIZATION_SUMMARY.md          ✅ Copied
├── PHASES_1_2_RECAP.md
├── requirements.txt
├── .gitignore
├── .env
├── .venv/                           (created by venv)
├── src/
│   └── garmin_ai/
│       ├── __init__.py
│       ├── config.py
│       ├── garmin_client.py
│       ├── fit_converter.py
│       ├── activities_analyzer.py
│       ├── form_analyzer.py
│       ├── target_profiles.py
│       └── synthetic_data_generator.py
└── data/
    ├── fit/                         (put your .fit files here)
    └── (other files generated by pipeline)
```

---

## ✨ You're Ready!

Once everything is in place:

```bash
# Copy FIT files
cp ~/Downloads/*.fit data/fit/

# Run the pipeline
./run.sh

# Check results
cat data/form_analysis.json | jq .overall_score
```

---

## 📚 Documentation Reference

After installation, refer to these docs based on your needs:

| Need | File | Location |
|------|------|----------|
| Quick start | CHEAT_SHEET.md | Root directory |
| Full usage | USAGE_SUMMARY.md | Root directory |
| Advanced | PIPELINE.md | Root directory |
| Technical | PHASES_1_2_RECAP.md | Root directory |
| Before/after | OPTIMIZATION_SUMMARY.md | Root directory |

All in your **project root directory** for easy access! 🎉
