# 📂 FILE PLACEMENT VISUAL GUIDE

## 🎯 THE ANSWER: PROJECT ROOT DIRECTORY

```
YOUR COMPUTER
└── Users/yourname/Projects/
    └── garmin-running-ai/              ← YOUR PROJECT ROOT
        ├── 🚀 pipeline.py              ← COPY pipeline.py HERE
        ├── 🚀 run.sh                   ← COPY run.sh HERE
        ├── 📄 USAGE_SUMMARY.md         ← COPY HERE
        ├── 📄 CHEAT_SHEET.md           ← COPY HERE
        ├── 📄 QUICKSTART_PIPELINE.md   ← COPY HERE
        ├── 📄 PIPELINE.md              ← COPY HERE
        ├── 📄 OPTIMIZATION_SUMMARY.md  ← COPY HERE
        ├── 📄 INSTALLATION_GUIDE.md    ← COPY HERE
        │
        ├── README.md                   (already here)
        ├── requirements.txt            (already here)
        ├── .gitignore                  (already here)
        │
        ├── src/
        │   └── garmin_ai/
        │       ├── config.py
        │       ├── garmin_client.py
        │       ├── fit_converter.py
        │       ├── activities_analyzer.py
        │       ├── form_analyzer.py
        │       ├── target_profiles.py
        │       └── synthetic_data_generator.py
        │
        └── data/
            ├── Activities.csv
            ├── fit/
            │   └── (put your .fit files here)
            ├── csv/
            ├── synthetic/
            └── pipeline.log
```

---

## 🔍 HOW TO FIND YOUR PROJECT ROOT

### Method 1: Using Terminal
```bash
# Navigate to your project directory
cd ~/Projects/garmin-running-ai/

# Verify you're in the root by checking for these files
ls -la README.md requirements.txt src/ data/

# If all those exist, you're in the root!
```

### Method 2: Using Finder (macOS)
1. Open Finder
2. Find your garmin-running-ai folder
3. You should see: README.md, requirements.txt, src/, data/
4. That folder IS your root

### Method 3: Using File Explorer (Windows)
1. Open File Explorer
2. Find your garmin-running-ai folder
3. You should see: README.md, requirements.txt, src/, data/
4. That folder IS your root

---

## 📋 COPY COMMAND (ONE LINE)

If all your files are in the same download folder:

```bash
# Navigate to your project root first
cd /path/to/garmin-running-ai/

# Copy all files at once
cp /path/to/downloads/pipeline.py /path/to/downloads/run.sh \
   /path/to/downloads/USAGE_SUMMARY.md \
   /path/to/downloads/CHEAT_SHEET.md \
   /path/to/downloads/QUICKSTART_PIPELINE.md \
   /path/to/downloads/PIPELINE.md \
   /path/to/downloads/OPTIMIZATION_SUMMARY.md \
   /path/to/downloads/INSTALLATION_GUIDE.md .
```

Or simpler:
```bash
# If downloads are all together
cd ~/Projects/garmin-running-ai/
cp ~/Downloads/pipeline.py .
cp ~/Downloads/run.sh .
cp ~/Downloads/*.md .
```

---

## ✅ VERIFICATION CHECKLIST

After copying files, verify they're in the right place:

```bash
# Navigate to your project root
cd /path/to/garmin-running-ai/

# Check each file
ls -la pipeline.py        # Should exist
ls -la run.sh             # Should exist and be executable
ls -la USAGE_SUMMARY.md   # Should exist
ls -la CHEAT_SHEET.md     # Should exist
ls -la PIPELINE.md        # Should exist

# Quick verification command
for file in pipeline.py run.sh USAGE_SUMMARY.md CHEAT_SHEET.md \
            QUICKSTART_PIPELINE.md PIPELINE.md OPTIMIZATION_SUMMARY.md \
            INSTALLATION_GUIDE.md; do
  [ -f "$file" ] && echo "✅ $file" || echo "❌ $file MISSING"
done
```

Expected output:
```
✅ pipeline.py
✅ run.sh
✅ USAGE_SUMMARY.md
✅ CHEAT_SHEET.md
✅ QUICKSTART_PIPELINE.md
✅ PIPELINE.md
✅ OPTIMIZATION_SUMMARY.md
✅ INSTALLATION_GUIDE.md
```

---

## 🚀 AFTER COPYING

### Make run.sh Executable
```bash
chmod +x run.sh
```

### Verify Executable
```bash
ls -la run.sh
# Should show: -rwxr-xr-x (with 'x' for executable)
```

### Test It Works
```bash
./run.sh --help
# Should show usage information
```

---

## 📍 COMMON MISTAKES & FIXES

### ❌ WRONG: Copying to src/garmin_ai/
```bash
# DON'T DO THIS
cp pipeline.py src/garmin_ai/
```

### ✅ RIGHT: Copying to Root
```bash
# DO THIS
cp pipeline.py .
# The "." means current directory (root)
```

---

### ❌ WRONG: Copying to data/
```bash
# DON'T DO THIS
cp pipeline.py data/
```

### ✅ RIGHT: Copying to Root
```bash
# DO THIS
cd /path/to/garmin-running-ai/
cp pipeline.py .
```

---

### ❌ WRONG: Forgetting to make run.sh executable
```bash
# This will fail:
./run.sh
# Error: Permission denied
```

### ✅ RIGHT: Make it executable first
```bash
chmod +x run.sh
./run.sh  # Now works!
```

---

## 🎯 SUMMARY

**One Simple Rule:**
```
Copy pipeline.py and run.sh (and all .md files) 
to the SAME directory where README.md and requirements.txt are.
```

That's your project root.

If you can see these files in a directory:
```
README.md
requirements.txt
src/  (directory)
data/ (directory)
```

Then that directory is your root, and that's where you copy all the new files.

---

## ✨ YOU'RE DONE WITH COPYING

Next steps:
1. `chmod +x run.sh`
2. `python -m venv .venv`
3. `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `./run.sh --dry-run` (test)
6. `./run.sh` (run for real)

Happy running! 🏃‍♂️
