import json
import subprocess

from garmin_ai.config import DATA_DIR


def run_full_pipeline():
    """
    Runs your existing pipeline (Phases 1–5) and returns ai_tips.json content.
    """

    # Option A — call your run.sh directly
    subprocess.run(["bash", "run.sh"], check=True)

    # Option B — call Python modules directly (we can do this later)

    # Load the final output
    tips_file = DATA_DIR / "ai_tips.json"
    if not tips_file.exists():
        raise FileNotFoundError("ai_tips.json not found after pipeline run")

    with open(tips_file, "r") as f:
        return json.load(f)
