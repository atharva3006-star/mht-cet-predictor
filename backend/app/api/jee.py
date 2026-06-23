"""
Stub route for JEE predictor — not implemented yet.
Returns a clear "coming soon" response so the frontend can show
the animated placeholder page without hitting a 404.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/predict/jee", tags=["JEE (coming soon)"])


@router.get("/status")
def jee_status():
    return {"available": False, "message": "JEE predictor is coming soon."}