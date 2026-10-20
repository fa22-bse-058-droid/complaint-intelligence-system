"""
Pydantic models for request/response validation.
Keeping this in a separate file so main.py stays focused on routing.
"""
from pydantic import BaseModel
from typing import List


class ComplaintRequest(BaseModel):
    complaint: str


class SimilarComplaint(BaseModel):
    complaint_id: int
    complaint_text: str
    category: str
    priority: str


class ComplaintResponse(BaseModel):
    category: str
    priority: str
    location: str
    duration: str
    problem_summary: str
    recommended_action: str
    similar_complaints: List[SimilarComplaint]