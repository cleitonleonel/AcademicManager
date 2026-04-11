"""
PDF router — generate and download PDF reports.
"""
from __future__ import annotations

import asyncio
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status, Header
from fastapi.responses import FileResponse

import json
from api.services import pdf_service as svc
from api.services import project_service as proj_svc

router = APIRouter(prefix="/projects", tags=["pdf"])


@router.post("/{project_id}/pdf", response_model=Dict[str, Any])
async def generate_pdf(project_id: str, x_pdf_options: str = Header(None)):
    """
    Generate a PDF for the given project.

    Uses the project's saved template JSON (or the default 4-section template).
    PDF generation can take a few seconds — it runs in a thread pool.
    """
    metadata = await asyncio.to_thread(proj_svc.get_project, project_id)
    if metadata is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado",
        )

    # Parse options from header if present
    options = None
    if x_pdf_options:
        try:
            options = json.loads(x_pdf_options)
        except:
            pass

    pdf_path = await asyncio.to_thread(svc.generate_pdf, project_id, metadata, options)

    if pdf_path is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha ao gerar o PDF. Verifique os logs.",
        )

    return {
        "message": "PDF gerado com sucesso",
        "pdf_path": pdf_path,
        "status": "success",
    }


@router.get("/{project_id}/pdf/download")
async def download_pdf(project_id: str):
    """
    Download the generated PDF for a project.

    Returns a binary file response.  The PDF must have been generated first
    via ``POST /api/projects/{id}/pdf``.
    """
    metadata = await asyncio.to_thread(proj_svc.get_project, project_id)
    if metadata is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado",
        )

    titulo = metadata.get("titulo", "")
    pdf_path = await asyncio.to_thread(svc.get_pdf_path, project_id, titulo)

    if pdf_path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF não encontrado. Gere o PDF primeiro.",
        )

    stem = titulo.replace(" ", "_").capitalize()
    return FileResponse(
        path=str(pdf_path),
        media_type="application/pdf",
        filename=f"{stem}.pdf",
    )
