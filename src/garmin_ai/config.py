"""
Configuration module for Garmin Running AI Pipeline
Defines paths, constants, and settings for all pipeline phases
"""

import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# DIRECTORY PATHS
# ═══════════════════════════════════════════════════════════════════════════════

# Get the base directory (project root)
BASE_DIR = Path(__file__).parent.parent.parent

# Main data directory
DATA_DIR = BASE_DIR / 'data'

# Data subdirectories
FIT_DIR = DATA_DIR / 'fit'                    # Input: Garmin FIT files
CSV_DIR = DATA_DIR / 'csv'                    # Intermediate: Converted FIT to CSV
SYNTHETIC_DIR = DATA_DIR / 'synthetic'        # Output: Synthetic training data

# Models directory (Phase 3 - ML models)
MODELS_DIR = BASE_DIR / 'src' / 'garmin_ai' / 'models'

# ═══════════════════════════════════════════════════════════════════════════════
# INPUT/OUTPUT FILE PATHS
# ═══════════════════════════════════════════════════════════════════════════════

# Phase 1 outputs
ACTIVITIES_CSV = DATA_DIR / 'Activities.csv'
RUNNING_PROFILE_JSON = DATA_DIR / 'running_profile.json'

# Phase 2 outputs
FORM_ANALYSIS_JSON = DATA_DIR / 'form_analysis.json'
TARGET_PROFILES_JSON = DATA_DIR / 'target_profiles.json'

# Synthetic data output
SYNTHETIC_ALL_PROFILES_CSV = SYNTHETIC_DIR / 'synthetic_all_profiles.csv'
SYNTHETIC_STEADY_RUNNER_CSV = SYNTHETIC_DIR / 'synthetic_steady_runner.csv'
SYNTHETIC_EFFICIENT_RUNNER_CSV = SYNTHETIC_DIR / 'synthetic_efficient_runner.csv'
SYNTHETIC_BALANCED_RUNNER_CSV = SYNTHETIC_DIR / 'synthetic_balanced_runner.csv'

# ═══════════════════════════════════════════════════════════════════════════════
# RUNNING FORM ANALYSIS PARAMETERS
# ═══════════════════════════════════════════════════════════════════════════════

# Cadence (steps per minute) - optimal range
CADENCE_MIN = 160
CADENCE_MAX = 180
CADENCE_IDEAL = 170

# Vertical oscillation (cm) - lower is more efficient
VERTICAL_OSCILLATION_MIN = 7.0
VERTICAL_OSCILLATION_MAX = 8.0
VERTICAL_OSCILLATION_IDEAL = 7.5

# Ground contact time (ms) - shorter is better
GROUND_CONTACT_TIME_MIN = 240
GROUND_CONTACT_TIME_MAX = 270
GROUND_CONTACT_TIME_IDEAL = 255

# Step speed loss (%) - lower is better (more consistent pace)
STEP_SPEED_LOSS_MIN = 4.0
STEP_SPEED_LOSS_MAX = 6.0
STEP_SPEED_LOSS_IDEAL = 5.0

# Heart rate efficiency (%)
HR_EFFICIENCY_MIN = 75
HR_EFFICIENCY_MAX = 85
HR_EFFICIENCY_IDEAL = 80

# ═══════════════════════════════════════════════════════════════════════════════
# SYNTHETIC DATA GENERATION PARAMETERS
# ═══════════════════════════════════════════════════════════════════════════════

# Number of synthetic runs to generate per profile
SYNTHETIC_RUNS_PER_PROFILE = 144

# Total synthetic runs (3 profiles × 144 runs each)
TOTAL_SYNTHETIC_RUNS = 432

# Profile names for synthetic data generation
SYNTHETIC_PROFILES = [
    'steady_runner',
    'efficient_runner',
    'balanced_runner'
]

# Profile characteristics (for synthetic generation)
PROFILE_CHARACTERISTICS = {
    'steady_runner': {
        'description': 'Consistent pace, stable metrics',
        'cadence_variation': 0.05,
        'form_stability': 'high',
    },
    'efficient_runner': {
        'description': 'High efficiency, optimized form',
        'cadence_variation': 0.03,
        'form_stability': 'very_high',
    },
    'balanced_runner': {
        'description': 'Balanced metrics across all dimensions',
        'cadence_variation': 0.07,
        'form_stability': 'medium',
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Log file location
LOG_FILE = DATA_DIR / 'pipeline.log'

# Log format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# ═══════════════════════════════════════════════════════════════════════════════
# PIPELINE PHASES CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PHASE_1_ENABLED = True  # Data Ingestion & FIT Conversion
PHASE_2_ENABLED = True  # Data Analysis & Form Scoring
PHASE_3_ENABLED = False  # ML Models (coming soon)
PHASE_4_ENABLED = False  # Generative AI Tips (coming soon)
PHASE5ENABLED = True  # ML Training & Prediction

# ═══════════════════════════════════════════════════════════════════════════════
# INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def init_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        DATA_DIR,
        FIT_DIR,
        CSV_DIR,
        SYNTHETIC_DIR,
        MODELS_DIR
    ]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create directory {directory}: {e}")

# Initialize directories when config is imported
init_directories()

def is_pipeline_mode():
    """Detect if running from pipeline.py"""
    return any('pipeline' in arg for arg in sys.argv)


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_config():
    """Validate that all required paths exist"""
    required_dirs = [DATA_DIR, FIT_DIR]
    
    for directory in required_dirs:
        if not directory.exists():
            print(f"Warning: Directory does not exist: {directory}")
    
    return True

# Validate on import
validate_config()
