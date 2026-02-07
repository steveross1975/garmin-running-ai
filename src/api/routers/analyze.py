from fastapi import APIRouter

from api.utils.pipeline_runner import run_full_pipeline

router = APIRouter()

@router.post("/analyze")
def analyze():
    """
    Runs the full Garmin AI pipeline and returns the final JSON.
    """
    result = run_full_pipeline()
    return result
