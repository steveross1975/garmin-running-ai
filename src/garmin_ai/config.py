"""Configuration module for Garmin Running AI pipeline.

Loads environment variables from .env file and defines project paths.
No credentials stored in code - everything via environment variables.
"""
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv  # [web:72][web:82]


def load_config() -> None:
    """Load .env file into environment variables."""
    load_dotenv()


# Load config immediately
load_config()

# Project root (2 levels up from src/garmin_ai/)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent

# Data directories (creates if missing)
DATA_DIR: Path = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))
FIT_DIR: Path = DATA_DIR / "fit"
CSV_DIR: Path = DATA_DIR / "csv"

# Garmin credentials (must be set in .env)
GARMIN_USERNAME: Optional[str] = os.getenv("GARMIN_USERNAME")
GARMIN_PASSWORD: Optional[str] = os.getenv("GARMIN_PASSWORD")

# Ensure directories exist
for directory in (DATA_DIR, FIT_DIR, CSV_DIR):
    directory.mkdir(parents=True, exist_ok=True)


def validate_config() -> None:
    """Validate required environment variables are set."""
    missing = []
    if not GARMIN_USERNAME:
        missing.append("GARMIN_USERNAME")
    if not GARMIN_PASSWORD:
        missing.append("GARMIN_PASSWORD")
    
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Create .env file with GARMIN_USERNAME and GARMIN_PASSWORD."
        )


if __name__ == "__main__":
    # Test the config
    validate_config()
    print("✅ Config loaded successfully")
    print(f"📁 DATA_DIR: {DATA_DIR}")
    print(f"📁 FIT_DIR:  {FIT_DIR}")
    print(f"📁 CSV_DIR:  {CSV_DIR}")
    print(f"🔐 Credentials: {'✅ Set' if GARMIN_USERNAME else '❌ Missing'}")
