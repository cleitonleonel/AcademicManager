"""
Pydantic models for the Academic Manager API.
"""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Project models
# ---------------------------------------------------------------------------

class ProjectCreate(BaseModel):
    """Payload to create or update an academic project."""
    titulo: str = Field(..., min_length=1, description="Título do projeto")
    aluno: str = Field(..., min_length=1, description="Nome do(s) aluno(s)")
    curso: str = Field(..., min_length=1, description="Nome do curso")
    disciplina: str = Field(..., min_length=1, description="Nome da disciplina")
    orientador: str = Field(..., min_length=1, description="Nome do orientador")
    instituicao: str = Field(
        default="FUNDAÇÃO DE ASSISTÊNCIA E EDUCAÇÃO",
        description="Nome da instituição",
    )
    unidade: str = Field(
        default="CENTRO UNIVERSITÁRIO ESPÍRITO-SANTENSE",
        description="Unidade de ensino",
    )
    local: str = Field(default="Vitória", description="Cidade")
    ano: Optional[int] = Field(None, ge=2000, le=2100, description="Ano do projeto")
    tipo: str = Field(default="GRADUAÇÃO", description="Tipo do trabalho")
    subtitulo: str = Field(default="", description="Subtítulo (opcional)")
    assignment: Optional[str] = Field(None, description="Enunciado/tarefa do trabalho")


class ProjectUpdate(ProjectCreate):
    """Same fields as create — full replacement."""
    pass


class ProjectResponse(BaseModel):
    """Project summary returned by list/detail endpoints."""
    id: str
    title: str
    description: str
    author: str
    status: str
    type: str
    created_date: Optional[str] = None
    updated_date: Optional[str] = None
    edit_count: int = 0
    folder: str


class ProjectDetailResponse(BaseModel):
    """Full project settings."""
    project: Dict[str, Any]


# ---------------------------------------------------------------------------
# Template / generation models
# ---------------------------------------------------------------------------

class GenerationRequest(BaseModel):
    """Request body for template generation."""
    type: Literal["ai", "existing"] = Field(
        ..., description="'ai' gera via Gemini, 'existing' carrega JSON salvo"
    )
    assignment: Optional[str] = Field(
        None, description="Enunciado usado quando type='ai'"
    )


# ---------------------------------------------------------------------------
# PDF models
# ---------------------------------------------------------------------------

class PDFResponse(BaseModel):
    message: str
    pdf_path: str
    status: str = "success"


# ---------------------------------------------------------------------------
# Stats / health
# ---------------------------------------------------------------------------

class StatsResponse(BaseModel):
    active_projects: int
    generated_pdfs: int
    in_progress: int
    total_files: int


class HealthResponse(BaseModel):
    status: str
    message: str
    version: str = "1.0.0"
    projects_count: int


# ---------------------------------------------------------------------------
# Generic response
# ---------------------------------------------------------------------------

class APIResponse(BaseModel):
    message: str
    status: str = "success"
    data: Optional[Dict[str, Any]] = None


class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]
