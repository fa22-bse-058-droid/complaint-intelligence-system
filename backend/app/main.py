"""
Complaint Intelligence System - FastAPI Backend
Phase 8: /api/analyze now calls the real Grok API via ai_service.py.
similar_complaints is still a placeholder empty list until Phase 9.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ComplaintRequest, ComplaintResponse
from app.ai_service import analyze_with_ai

app = FastAPI(title="Complaint Intelligence System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Complaint Intelligence backend is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/api/analyze", response_model=ComplaintResponse)
def analyze_complaint(request: ComplaintRequest):
    if not request.complaint or not request.complaint.strip():
        raise HTTPException(status_code=400, detail="Complaint text cannot be empty")

    try:
        ai_result = analyze_with_ai(request.complaint)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"AI analysis failed: {e}")

    return ComplaintResponse(
        category=ai_result["category"],
        priority=ai_result["priority"],
        location=ai_result["location"],
        duration=ai_result["duration"],
        problem_summary=ai_result["problem_summary"],
        recommended_action=ai_result["recommended_action"],
        similar_complaints=[],  # Phase 9 will fill this in
    )