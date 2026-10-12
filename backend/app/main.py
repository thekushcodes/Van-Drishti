
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analysis_runs import router as analysis_runs_router
from app.routes.detection import router as detection_router
from app.routes.intelligence import router as intelligence_router
from app.routes.detections import router as detections_router
from app.routes.reviews import router as reviews_router
from app.routes.alerts import router as alerts_router


# Resolve directories relative to the backend folder.
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
EVIDENCE_DIR = BASE_DIR / "evidence"

# Create runtime directories if they don't exist.
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="VanDrishti M1 Backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "https://vandrishti-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/outputs",
    StaticFiles(directory=str(OUTPUTS_DIR)),
    name="outputs",
)

app.mount(
    "/evidence",
    StaticFiles(directory=str(EVIDENCE_DIR)),
    name="evidence",
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "module": "M1-backend",
    }


app.include_router(analysis_runs_router)
app.include_router(detection_router)
app.include_router(intelligence_router)
app.include_router(detections_router)
app.include_router(reviews_router)
app.include_router(alerts_router)