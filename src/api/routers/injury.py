from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

INJURY_PROTOCOLS = {
    "achilles": {
        "recovery_weeks": [4, 8],
        "load_rules": [
            "Reduce weekly volume by 30–50% for the first 2 weeks",
            "Avoid hills and speed work until pain < 2/10",
            "Increase load by max 10% per week"
        ],
        "exercises": [
            "Eccentric heel drops: 3x15 twice daily",
            "Seated calf raises: 3x12 moderate load",
            "Isometric calf holds: 5x45s"
        ],
        "return_to_run": [
            "Pain ≤ 2/10 during and after easy runs",
            "No morning stiffness increase for 3 consecutive days"
        ]
    }
}

class InjuryRequest(BaseModel):
    injury_type: str
    pain_level: int
    onset_days: int
    current_weekly_km: float

@router.post("/injury")
def injury_handler(req: InjuryRequest):
    protocol = INJURY_PROTOCOLS.get(req.injury_type.lower())
    if not protocol:
        return {"error": "Unknown injury type"}

    # Personalization example
    min_w, max_w = protocol["recovery_weeks"]
    if req.pain_level >= 7:
        max_w += 2

    return {
        "recovery_time_weeks": [min_w, max_w],
        "load_adjustments": protocol["load_rules"],
        "recommended_exercises": protocol["exercises"],
        "return_to_run_criteria": protocol["return_to_run"]
    }
