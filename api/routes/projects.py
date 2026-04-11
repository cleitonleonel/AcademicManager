"""
Projects router — CRUD for academic projects.
"""
from __future__ import annotations

import asyncio
from typing import Any, Dict, List

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from api.models import (
    APIResponse,
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
)
from api.services import project_service as svc

router = APIRouter(prefix="/projects", tags=["projects"])


# ---------------------------------------------------------------------------
# List & create
# ---------------------------------------------------------------------------

@router.get("", response_model=ProjectListResponse)
async def list_projects():
    """List all academic projects."""
    projects_raw = await asyncio.to_thread(svc.list_projects)
    projects = [ProjectResponse(**p) for p in projects_raw]
    return ProjectListResponse(projects=projects)


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate):
    """Create a new academic project."""
    data = payload.model_dump()
    try:
        folder, metadata = await asyncio.to_thread(svc.create_project, data)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar projeto: {exc}",
        )
    return {
        "message": "Projeto criado com sucesso",
        "project_folder": folder,
        "metadata": metadata,
        "status": "success",
    }


# ---------------------------------------------------------------------------
# Get / update / delete single project
# ---------------------------------------------------------------------------

@router.get("/{project_id}", response_model=Dict[str, Any])
async def get_project(project_id: str):
    """Return settings for a specific project."""
    settings = await asyncio.to_thread(svc.get_project, project_id)
    if settings is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado",
        )
    return {"project": settings}


@router.put("/{project_id}", response_model=Dict[str, Any])
async def update_project(project_id: str, payload: ProjectUpdate):
    """Update an existing project's metadata."""
    data = payload.model_dump()
    result = await asyncio.to_thread(svc.update_project, project_id, data)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado",
        )
    return {
        "message": "Projeto atualizado com sucesso",
        "project": result,
        "status": "success",
    }


@router.delete("/{project_id}", response_model=APIResponse)
async def delete_project(project_id: str):
    """Remove a project and all its files."""
    deleted = await asyncio.to_thread(svc.delete_project, project_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado",
        )
    return APIResponse(message="Projeto removido com sucesso")


# ---------------------------------------------------------------------------
# Files within a project
# ---------------------------------------------------------------------------

@router.get("/{project_id}/files", response_model=Dict[str, Any])
async def list_project_files(project_id: str):
    """List all files (recursively) inside a project directory."""
    files = await asyncio.to_thread(svc.list_project_files, project_id)
    if files is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado",
        )
    return {"files": files}


@router.post("/{project_id}/attachments", response_model=Dict[str, Any])
async def upload_attachment(project_id: str, file: UploadFile = File(...)):
    """Upload a file to the project's attachments folder."""
    # Verify project exists
    settings = await asyncio.to_thread(svc.get_project, project_id)
    if settings is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado",
        )
    content = await file.read()
    try:
        dest = await asyncio.to_thread(
            svc.save_attachment, project_id, file.filename, content
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar arquivo: {exc}",
        )
    return {
        "message": "Arquivo enviado com sucesso",
        "filename": file.filename,
        "path": dest,
        "status": "success",
    }
