from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    MhtcetPredictRequest,
    MhtcetPredictResponse,
    CollegeResult,
    CategoryListResponse,
    CategoryOption,
    UniversityListResponse,
)
from app.core.config import get_engine, get_category_map

router = APIRouter(prefix="/predict/mhtcet", tags=["MHT-CET"])


@router.post("", response_model=MhtcetPredictResponse)
def predict_mhtcet(payload: MhtcetPredictRequest):
    engine = get_engine()

    cat_map = get_category_map()
    valid_categories = set(cat_map["categories"].keys())
    if payload.category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown category code '{payload.category}'. See /predict/mhtcet/categories for valid options.",
        )

    results = engine.predict(
        percentile=payload.percentile,
        category=payload.category,
        home_university=payload.home_university,
        branch_keyword=payload.branch,
        region=payload.region,
    )

    college_results = [CollegeResult(**r.__dict__) for r in results]
    safe = [r for r in college_results if r.bucket == "Safe"]
    target = [r for r in college_results if r.bucket == "Target"]
    reach = [r for r in college_results if r.bucket == "Reach"]

    return MhtcetPredictResponse(
        total_results=len(college_results),
        safe=safe,
        target=target,
        reach=reach,
    )


@router.get("/categories", response_model=CategoryListResponse)
def list_categories():
    cat_map = get_category_map()
    options = [
        CategoryOption(code=code, label=info["label"])
        for code, info in cat_map["categories"].items()
    ]
    options.sort(key=lambda o: o.label)
    return CategoryListResponse(categories=options)


@router.get("/universities", response_model=UniversityListResponse)
def list_universities():
    engine = get_engine()
    unis = (
        engine.df["college_home_university"]
        .dropna()
        .unique()
        .tolist()
    )
    unis = sorted(set(unis))
    return UniversityListResponse(universities=unis)