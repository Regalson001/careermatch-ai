# schemas.py

from pydantic import BaseModel, Field
from typing import Literal


class SkillResult(BaseModel):
    name: str
    importance: Literal["high", "medium"]
    matched: bool
    evidence: str = ""


class BulletSuggestion(BaseModel):
    original_context: str
    suggested_bullet: str
    reason: str


class MatchAnalysis(BaseModel):
    filename: str
    match_score: int = Field(ge=0, le=100)
    score_label: str
    summary: str
    matched_skills: list[str]
    missing_skills: list[str]
    required_skills: list[SkillResult]
    strengths: list[str]
    recommendations: list[str]
    bullet_suggestions: list[BulletSuggestion]
    disclaimer: str
