"""
AI router — template generation via Gemini and assignment management.
"""
from __future__ import annotations

import asyncio
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status, Header

from api.models import GenerationRequest
from api.services import ai_service as svc
from api.services import project_service as proj_svc

router = APIRouter(tags=["ai"])


# ---------------------------------------------------------------------------
# Assignments
# ---------------------------------------------------------------------------

@router.get("/assignments", response_model=Dict[str, List[str]])
async def list_assignments():
    """List available assignment files (enunciados)."""
    assignments = await asyncio.to_thread(svc.list_assignments)
    return {"assignments": assignments}


# ---------------------------------------------------------------------------
# Template generation & retrieval
# ---------------------------------------------------------------------------

@router.get("/projects/{project_id}/template", response_model=Dict[str, Any])
async def get_template(project_id: str):
    """Return the current template JSON for a project (existing or default)."""
    settings = await asyncio.to_thread(proj_svc.get_project, project_id)
    if settings is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado",
        )
    template = await asyncio.to_thread(svc.load_existing_template, project_id)
    return {"template": template}


@router.post("/projects/{project_id}/generate", response_model=Dict[str, Any])
async def generate_content(
    project_id: str, 
    request: GenerationRequest, 
    authorization: str = Header(None)
):
    """
    Generate content for a project.

    - ``type="existing"`` — loads the saved template JSON (or the default).
    - ``type="ai"`` — calls Gemini API to generate a new template.
      An ``assignment`` string is required for AI generation.
    """
    settings = await asyncio.to_thread(proj_svc.get_project, project_id)
    if settings is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado",
        )

    if request.type == "existing":
        template = await asyncio.to_thread(svc.load_existing_template, project_id)
        return {
            "message": "Template existente carregado",
            "template": template,
            "type": "existing",
            "status": "success",
        }

    # AI generation
    if not request.assignment:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="O campo 'assignment' é obrigatório para geração via IA.",
        )

    # Extract key from "Bearer <key>" if present
    api_key_override = None
    if authorization and authorization.startswith("Bearer "):
        api_key_override = authorization.replace("Bearer ", "").strip()

    template = await asyncio.to_thread(
        svc.generate_ai_template, project_id, request.assignment, api_key_override
    )

    if template is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha ao gerar template via IA. Verifique a API key e os logs.",
        )

    return {
        "message": "Template gerado via IA com sucesso",
        "template": template,
        "type": "ai_generated",
        "status": "success",
    }
