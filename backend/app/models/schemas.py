"""
Pydantic models defining the request and response shape for the
/predict/mhtcet endpoint.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class MhtcetPredictRequest(BaseModel):
    percentile: float = Field(..., ge=0, le=100, description="MHT-CET percentile score")
    category: str = Field(..., description="Category code, e.g. GOPENS, LOBCS, etc.")
    home_university: Optional[str] = Field(
        None, description="Student's home university (exact name as in dropdown)"
    )
    branch: Optional[str] = Field(
        None, description="Optional keyword to filter branch, e.g. 'Computer'"
    )
    region: Optional[str] = Field(None, description="Optional preferred region filter")

    @field_validator("category")
    @classmethod
    def category_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("category must not be empty")
        return v.strip()


class CollegeResult(BaseModel):
    college_code: str
    college_name: str
    branch_code: str
    branch_name: str
    region: Optional[str] = None
    college_home_university: Optional[str] = None
    category: str
    seat_pool: str
    latest_cutoff_percentile: float
    previous_cutoff_percentile: Optional[float] = None
    trend: str
    bucket: str


class MhtcetPredictResponse(BaseModel):
    total_results: int
    safe: List[CollegeResult]
    target: List[CollegeResult]
    reach: List[CollegeResult]


class CategoryOption(BaseModel):
    code: str
    label: str


class CategoryListResponse(BaseModel):
    categories: List[CategoryOption]


class UniversityListResponse(BaseModel):
    universities: List[str]