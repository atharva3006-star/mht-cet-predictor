from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback

from app.api import mhtcet, jee

app = FastAPI(
    title="College Predictor API",
    description="Predicts likely colleges based on MHT-CET / JEE percentile.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "traceback": tb},
    )


app.include_router(mhtcet.router)
app.include_router(jee.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "College Predictor API is running."}


@app.get("/health")
def health():
    return {"status": "healthy"}