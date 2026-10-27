"""
Academic Manager — FastAPI application entry point.

Serves:
  - REST API under /api/*
  - Frontend static files at /
  - Interactive docs at /docs and /redoc
"""
from __future__ import annotations

import asyncio
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from api.models import HealthResponse, StatsResponse
from api.routes import ai, pdf, pptx, projects, system
from api.services import project_service as proj_svc

# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Academic Manager API",
    description=(
        "API para gerenciamento e geração automatizada de trabalhos acadêmicos em PDF."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(system.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(pdf.router, prefix="/api")
app.include_router(pptx.router, prefix="/api")
app.include_router(ai.router, prefix="/api")

# ---------------------------------------------------------------------------
# Core API endpoints
# ---------------------------------------------------------------------------


@app.get("/api/health", response_model=HealthResponse, tags=["system"])
async def health():
    """API health check."""
    count = len(await asyncio.to_thread(proj_svc.list_projects))
    return HealthResponse(
        status="ok",
        message="Academic Manager API is running",
        projects_count=count,
    )


@app.get("/api/stats", response_model=StatsResponse, tags=["system"])
async def stats():
    """Aggregate counters for the dashboard."""
    data = await asyncio.to_thread(proj_svc.get_stats)
    return StatsResponse(**data)


# ---------------------------------------------------------------------------
# Global exception handler
# ---------------------------------------------------------------------------


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Erro interno do servidor", "detail": str(exc), "status": "error"},
    )


# ---------------------------------------------------------------------------
# Static files — MUST be mounted AFTER routes so /api/* takes precedence
# ---------------------------------------------------------------------------

_FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

if _FRONTEND_DIR.exists():
    # Serve frontend JS/CSS sub-directories under their original paths
    # so the HTML references like /frontend/css/main.css keep working.
    app.mount("/frontend", StaticFiles(directory=str(_FRONTEND_DIR)), name="frontend")

    # Serve index.html at root
    from fastapi.responses import HTMLResponse

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def serve_index():
        index = _FRONTEND_DIR / "index.html"
        return HTMLResponse(index.read_text(encoding="utf-8"))
