import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from app.core.config import settings
from app.database.session import Base, engine
from app.database.seed import seed_database

from app.api.auth import router as auth_router
from app.api.student import router as student_router
from app.api.dashboard import router as dashboard_router
from app.api.subjects import router as subjects_router
from app.api.quiz import router as quiz_router
from app.api.performance import router as performance_router
from app.api.recommendations import router as recommendations_router
from app.api.prediction import router as prediction_router
from app.api.admin import router as admin_router

# Initialize DB tables & seed data
Base.metadata.create_all(bind=engine)
try:
    seed_database()
except Exception as e:
    print(f"Seed warning: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Enable CORS for local development and browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers under /api
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(student_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(subjects_router, prefix=settings.API_V1_STR)
app.include_router(quiz_router, prefix=settings.API_V1_STR)
app.include_router(performance_router, prefix=settings.API_V1_STR)
app.include_router(recommendations_router, prefix=settings.API_V1_STR)
app.include_router(prediction_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)

# Serve Frontend static directory if present
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "public"))
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    def read_root():
        return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/health")
def health_check():
    return {"status": "healthy", "project": settings.PROJECT_NAME, "version": settings.VERSION}
