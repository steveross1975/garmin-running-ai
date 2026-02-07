# src/api/main.py
from fastapi import FastAPI
from pydantic import BaseModel

from api.routers import analyze, injury, upload

app = FastAPI(title="Garmin Running AI API") 
app.include_router(upload.router) 
app.include_router(analyze.router) 
app.include_router(injury.router)

class AnalyzeResponse(BaseModel):
    form_score: float
    message: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze():
    # TODO: here we will call your existing pipeline:
    # - run activities_analyzer
    # - run form_analyzer
    # - run Phase 5 model
    # For now, return a dummy response.
    return AnalyzeResponse(
        form_score=75.3,
        message="Stub analysis – pipeline integration coming next."
    )
