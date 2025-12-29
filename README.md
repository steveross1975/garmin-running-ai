# Garmin Running AI

# Garmin Running AI - Complete Roadmap

## Current Status ✅

### Data You Have
1. **Track FIT files** (3 runs)
   - Per-second: timestamp, HR, cadence, distance, speed, power, GPS
   - No per-second running dynamics (VO, GCT, SSL) in export format

2. **Activity CSV files** (sample-by-sample running data)
   - Per-second metrics from 21328723558_ACTIVITY.csv
   - 851 samples × 14 columns
   
3. **Activities.csv** (master summary)
   - 3 complete running activities with all Garmin metrics:
     - Cadence: 160-170 spm (avg)
     - Vertical Oscillation: 8.5-8.8 cm
     - Ground Contact Time: 267-274 ms
     - Step Speed Loss: 20.2-20.5 cm/s (7.06-7.56%)
     - GCT Balance: 50% L / 50% R
     - HR: 145-156 bpm avg, 165-180 max
     - Aerobic TE: 4.2-5.0 per run

4. **running_profile.json**
   - Your baseline metrics across all 3 runs
   - Foundation for AI models

---

## Phase 2: Data Analysis & Baselines (THIS PHASE)

### 2.1 Compute Your Current Running Form Score
**Goal**: Create a "form efficiency" baseline from your actual data

**Build**: `src/garmin_ai/form_analyzer.py`
- Load Activities.csv + running_profile.json
- Compare your metrics to **sports science benchmarks** for 50yo runners
- Score: cadence, VO, GCT, SSL, HR zones
- Output: JSON with current scores + improvement gaps

**Key comparisons** (from research):
- **Cadence**: Target 165-180 spm (yours: 160-170) → small gap ✓
- **Vertical Oscillation**: <8cm (optimal), <10cm (good) → yours: 8.5-8.8 ✓
- **Ground Contact Time**: <250ms (elite), <280ms (good) → yours: 267-274 ✓
- **Step Speed Loss**: <5% (elite), <10% (good) → yours: 7.06-7.56 ✓
- **HR Efficiency**: Max HR / Age-predicted max → assess recovery zones

**Output**: Form report with scores, gaps, and priority areas

---

### 2.2 Define Experienced 50yo Runner Profiles
**Goal**: Create realistic "target" profiles to learn from

**Build**: `src/garmin_ai/target_profiles.py`
- Use research + your data to define 3 target runner archetypes:
  1. **Steady Runner** (conservative, focus: endurance)
     - Cadence: 155-165 spm
     - VO: 7-8 cm
     - GCT: 250-260 ms
     - SSL: 5-6%
  
  2. **Efficient Runner** (optimized form, focus: economy)
     - Cadence: 170-180 spm
     - VO: 7-7.5 cm
     - GCT: 240-250 ms
     - SSL: 4-5%
  
  3. **Balanced Runner** (mix, focus: speed + endurance)
     - Cadence: 165-175 spm
     - VO: 7.5-8.5 cm
     - GCT: 250-270 ms
     - SSL: 5-7%

**Output**: JSON profiles with distributions + zone ranges

---

### 2.3 Generate Synthetic Training Data
**Goal**: Create realistic "intermediate" runs between current state and targets

**Build**: `src/garmin_ai/synthetic_data_generator.py`
- Input: Your current metrics + target profiles
- For each metric (cadence, VO, GCT, SSL, HR):
  - Create 10-20 "intermediate" data points
  - Use Bezier curves or spline interpolation between current → target
  - Add realistic noise (±5-10%)
- Generate 50-100 synthetic "training scenarios"

**Example**: Current cadence 167 → target 175
- Week 1: 167 spm
- Week 2: 168.5 spm
- Week 3: 170 spm
- ...
- Week 8: 175 spm (with small daily variations)

**Output**: CSV with synthetic runs (activity_id, timestamp, metrics, label)

---

## Phase 3: Machine Learning Models (NEXT PHASE)

### 3.1 Form Efficiency Predictor
**Model Type**: LSTM (time-series) or Gradient Boosting (tabular)
**Input**: HR, cadence, distance, power, pace (from FIT)
**Output**: Predicted form score (0-100)
**Task**: Learn relationship between raw metrics → form quality

### 3.2 Running Dynamics Approximator
**Model Type**: Regression (Linear or XGBoost)
**Input**: Your available metrics (HR, cadence, pace, power)
**Output**: Approximate vertical oscillation, GCT, SSL
**Task**: Given what you measure → what likely form metrics are

### 3.3 Zone Optimizer
**Model Type**: Clustering + Classification
**Input**: HR, pace, cadence per activity
**Output**: Optimal training zones for your physiology
**Task**: Identify your personal HR zones + cadence zones

---

## Phase 4: Generative AI Tips (FINAL PHASE)

### 4.1 Form Analysis Report Generator
**Tool**: OpenAI API or local LLM (Mistral/Ollama)
**Input**: Your metrics + model predictions + targets
**Output**: Personalized form improvement tips

**Example output**:
```
📊 Your Running Form Analysis (2025-12-28)

✅ Strengths:
- Excellent cadence efficiency at 160 spm for easy runs
- GCT balance is nearly perfect (50.2% L / 49.8% R)
- HR recovery: drops quickly after runs → good fitness

🎯 Focus Areas:
- Vertical oscillation: 8.6cm (target: 8.0cm)
  → Work on: lighter footstrike, knee lift drills
- Step Speed Loss: 7.5% (target: 5-6%)
  → Work on: power training, hill repeats
- Cadence on tempo runs: increase from 170 to 175 spm
  → Work on: metronome-based tempo runs

💡 Next 4 Weeks:
Week 1-2: Focus on cadence drills (3x per week)
Week 3-4: Add hill repeats for SSL improvement
```

---

## Immediate Next Steps (Today)

### ✅ DONE
- [x] Setup professional project structure (src, .venv, .gitignore, GitHub)
- [x] Create local FIT file handler (garmin_client.py)
- [x] Build FIT → CSV converter (fit_converter.py)
- [x] Create activity analyzer (activities_analyzer.py)
- [x] Extract running profile (running_profile.json)

### ⏭️ TODO (Priority Order)

**PHASE 2.1** (1-2 hours): Form Analyzer
```python
# Build form_analyzer.py
- Load your Activities.csv
- Compare to benchmarks
- Generate form scores
- Identify gaps
```

**PHASE 2.2** (1-2 hours): Target Profiles
```python
# Build target_profiles.py
- Define 3 experienced runner archetypes
- Create realistic target ranges
- Output JSON profiles
```

**PHASE 2.3** (2-3 hours): Synthetic Data
```python
# Build synthetic_data_generator.py
- Interpolate current → targets
- Generate 50-100 training scenarios
- Output training dataset CSV
```

**PHASE 3.1** (3-4 hours): First ML Model
```python
# Build form_efficiency_model.py
- Load synthetic data
- Train LSTM on time-series
- Evaluate on your real runs
- Save model weights
```

**PHASE 4.1** (1-2 hours): Generative Tips
```python
# Build tips_generator.py
- Use OpenAI API or local LLM
- Input: your metrics + model predictions
- Output: personalized form tips
```

---

## Recommended Order (This Week)

**Today**: 
- Form Analyzer (PHASE 2.1) ← START HERE
- Commit to GitHub

**Tomorrow**:
- Target Profiles (PHASE 2.2)
- Synthetic Data Generator (PHASE 2.3)

**Next 2 days**:
- First ML Model (PHASE 3.1)
- Generative Tips (PHASE 4.1)

**By end of week**:
- Complete end-to-end pipeline
- Test on your 3 runs
- Refine + iterate

---

## Key Insights from Your Data

### Your Current Profile (baseline for 50yo, 3mo runner)
- **Strengths**: Good cadence control, balanced GCT, efficient HR zones
- **Improvement areas**: Vertical oscillation & step speed loss
- **Potential**: You're already in good form for a beginner → significant room to optimize

### Target by 2027 (top 30-40%)
- Focus on 3 areas: cadence consistency, step speed loss reduction, vertical oscillation
- Realistic gains: 5-10 spm cadence increase, 2-3% SSL reduction, 0.5-1cm VO decrease
- These gains = 2-5% overall pace improvement + better injury resilience

### Training Strategy
- Your metrics suggest: tempo runs + hill repeats for SSL
- Cadence work: metronome drills
- Strength: 2x/week (glutes, core, calves)

---

## Success Metrics

By end of Phase 4, your pipeline will:
1. ✅ Load any new run's FIT/CSV
2. ✅ Score your form across 5 dimensions
3. ✅ Compare to your past + targets
4. ✅ Predict likely running dynamics
5. ✅ Generate personalized AI tips
6. ✅ Track progress month-over-month
7. ✅ Cost <$1/month to run

**All local or free cloud** (Google Colab, Streamlit Cloud).

---

## Architecture Summary

```
data/
├── Activities.csv ← Master file
├── running_profile.json ← Current baseline
├── fit/ ← Track files
├── csv/ ← Converted FITs
└── synthetic/ ← Generated training data

src/garmin_ai/
├── garmin_client.py ✅
├── fit_converter.py ✅
├── activities_analyzer.py ✅
├── form_analyzer.py ← BUILD NEXT
├── target_profiles.py ← BUILD NEXT
├── synthetic_data_generator.py ← BUILD NEXT
├── models/ ← PHASE 3
│   ├── form_efficiency_model.py
│   ├── dynamics_approximator.py
│   └── zone_optimizer.py
└── tips_generator.py ← PHASE 4
```

---

## Decision Point

**Option A**: Build full pipeline (Phases 2-4) = 15-20 hours, complete AI system
**Option B**: Stop at Phase 2.1, focus on immediate form analysis = 2-3 hours, quick insights

**Recommendation**: Start with **Phase 2.1 (Form Analyzer)** - gives you immediate insights about your running, then decide if you want the full ML pipeline.

---

**Ready to build Phase 2.1?** Say "build form analyzer" and we'll create it in the next response! 🚀