"""
Integration tests for the Academic Manager FastAPI endpoints.

Uses FastAPI's TestClient (built on httpx) so no real server needs to run.
All filesystem side-effects are isolated under a temporary directory by
monkey-patching ``academic_manager.config.settings.Config.BASE_DIR`` before
each test.

Run with:
    poetry run pytest tests/test_api.py -v
"""
from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Patch Config BEFORE importing the app so every module reads the temp dir.
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def isolated_project_dir(tmp_path: Path):
    """
    Redirect all file operations to a unique temp directory for each test.
    The patch is applied at the Config class level so every service module
    picks it up automatically.
    """
    from academic_manager.config.settings import Config

    original_base = Config.BASE_DIR
    original_assignments = Config.ASSIGNMENTS_DIR

    Config.BASE_DIR = tmp_path / "academic_projects"
    Config.ASSIGNMENTS_DIR = Config.BASE_DIR / "assignments"
    Config.BASE_DIR.mkdir(parents=True, exist_ok=True)
    Config.ASSIGNMENTS_DIR.mkdir(parents=True, exist_ok=True)

    yield tmp_path

    Config.BASE_DIR = original_base
    Config.ASSIGNMENTS_DIR = original_assignments


@pytest.fixture(scope="module")
def client() -> Generator:
    """Return a TestClient backed by the real FastAPI app."""
    from api.main import app
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SAMPLE_PROJECT = {
    "titulo": "Sistemas Distribuídos com IA",
    "aluno": "João Silva",
    "curso": "Engenharia de Software",
    "disciplina": "Computação Distribuída",
    "orientador": "Prof. Maria Santos",
    "instituicao": "FAESA",
    "unidade": "Centro Universitário Espírito-Santense",
    "local": "Vitória",
    "ano": 2025,
    "tipo": "GRADUAÇÃO",
    "subtitulo": "",
    "assignment": "Implemente um sistema distribuído usando Python.",
}


def _create_project(client: TestClient) -> str:
    """Helper: POST /api/projects and return the project_folder."""
    res = client.post("/api/projects", json=SAMPLE_PROJECT)
    assert res.status_code == 201, res.text
    return res.json()["project_folder"]


# ---------------------------------------------------------------------------
# System
# ---------------------------------------------------------------------------

class TestSystem:
    def test_health(self, client: TestClient):
        res = client.get("/api/health")
        assert res.status_code == 200
        body = res.json()
        assert body["status"] == "ok"
        assert "projects_count" in body

    def test_stats(self, client: TestClient):
        res = client.get("/api/stats")
        assert res.status_code == 200
        body = res.json()
        assert "active_projects" in body
        assert "generated_pdfs" in body

    def test_root_serves_frontend(self, client: TestClient):
        """Root / must return an HTML page (the frontend index.html)."""
        res = client.get("/")
        assert res.status_code == 200
        assert "text/html" in res.headers["content-type"]
        assert "Academic Manager" in res.text


# ---------------------------------------------------------------------------
# Projects CRUD
# ---------------------------------------------------------------------------

class TestProjectsCRUD:
    def test_list_projects_empty(self, client: TestClient):
        res = client.get("/api/projects")
        assert res.status_code == 200
        assert res.json()["projects"] == []

    def test_create_project(self, client: TestClient):
        res = client.post("/api/projects", json=SAMPLE_PROJECT)
        assert res.status_code == 201
        body = res.json()
        assert body["status"] == "success"
        assert "project_folder" in body
        # Folder must actually exist on disk
        from academic_manager.config.settings import Config
        folder = body["project_folder"]
        assert (Config.BASE_DIR / folder).is_dir()

    def test_create_project_missing_required_field(self, client: TestClient):
        bad = {k: v for k, v in SAMPLE_PROJECT.items() if k != "titulo"}
        res = client.post("/api/projects", json=bad)
        assert res.status_code == 422  # Pydantic validation error

    def test_list_projects_after_create(self, client: TestClient):
        _create_project(client)
        res = client.get("/api/projects")
        assert res.status_code == 200
        projects = res.json()["projects"]
        assert len(projects) >= 1
        assert projects[0]["title"] == SAMPLE_PROJECT["titulo"]

    def test_assignment_controls_progress_status(self, client: TestClient):
        project_without_assignment = {
            key: value for key, value in SAMPLE_PROJECT.items() if key != "assignment"
        }
        res = client.post("/api/projects", json=project_without_assignment)
        assert res.status_code == 201, res.text
        folder = res.json()["project_folder"]
        res = client.get("/api/projects")
        assert res.status_code == 200
        assert res.json()["projects"][0]["status"] == "draft"

        from academic_manager.config.settings import Config
        (Config.ASSIGNMENTS_DIR / f"{folder}.md").write_text(
            "Enunciado do trabalho", encoding="utf-8"
        )

        res = client.get("/api/projects")
        assert res.status_code == 200
        assert res.json()["projects"][0]["status"] == "progress"

    def test_get_project(self, client: TestClient):
        folder = _create_project(client)
        res = client.get(f"/api/projects/{folder}")
        assert res.status_code == 200
        project = res.json()["project"]
        assert project["titulo"] == SAMPLE_PROJECT["titulo"]
        assert project["aluno"] == SAMPLE_PROJECT["aluno"]

    def test_get_project_not_found(self, client: TestClient):
        res = client.get("/api/projects/does_not_exist")
        assert res.status_code == 404

    def test_update_project(self, client: TestClient):
        folder = _create_project(client)
        updated = {**SAMPLE_PROJECT, "titulo": "Título Atualizado", "local": "São Paulo"}
        res = client.put(f"/api/projects/{folder}", json=updated)
        assert res.status_code == 200
        body = res.json()
        assert body["project"]["titulo"] == "Título Atualizado"
        assert body["project"]["local"] == "São Paulo"

    def test_update_project_not_found(self, client: TestClient):
        res = client.put("/api/projects/ghost", json=SAMPLE_PROJECT)
        assert res.status_code == 404

    def test_delete_project(self, client: TestClient):
        folder = _create_project(client)
        res = client.delete(f"/api/projects/{folder}")
        assert res.status_code == 200
        assert res.json()["status"] == "success"
        # Confirm gone
        from academic_manager.config.settings import Config
        assert not (Config.BASE_DIR / folder).exists()

    def test_delete_project_not_found(self, client: TestClient):
        res = client.delete("/api/projects/ghost")
        assert res.status_code == 404


# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------

class TestProjectFiles:
    def test_list_files(self, client: TestClient):
        folder = _create_project(client)
        res = client.get(f"/api/projects/{folder}/files")
        assert res.status_code == 200
        files = res.json()["files"]
        # settings.json should always be present after project creation
        names = [f["name"] for f in files]
        assert "settings.json" in names

    def test_upload_attachment(self, client: TestClient):
        folder = _create_project(client)
        file_content = b"fake image bytes"
        res = client.post(
            f"/api/projects/{folder}/attachments",
            files={"file": ("test_image.jpg", file_content, "image/jpeg")},
        )
        assert res.status_code == 200
        body = res.json()
        assert body["filename"] == "test_image.jpg"
        # Verify the file is on disk
        from academic_manager.config.settings import Config
        dest = Config.BASE_DIR / folder / "attachments" / "test_image.jpg"
        assert dest.exists()
        assert dest.read_bytes() == file_content


# ---------------------------------------------------------------------------
# PDF (mocked — PDFGenerator is heavy)
# ---------------------------------------------------------------------------

class TestPDF:
    def test_generate_pdf(self, client: TestClient):
        folder = _create_project(client)

        with patch("api.services.pdf_service.PDFGenerator") as MockGen:
            # Simulate successful generation: create a dummy PDF file
            from academic_manager.config.settings import Config
            titulo = SAMPLE_PROJECT["titulo"]
            stem = titulo.replace(" ", "_").capitalize()
            pdf_path = Config.BASE_DIR / folder / f"{stem}.pdf"

            def fake_generate_pdf(project_name, metadata, template, options=None):
                pdf_path.write_bytes(b"%PDF-1.4 fake")
                return True

            MockGen.return_value.generate_pdf.side_effect = fake_generate_pdf

            res = client.post(f"/api/projects/{folder}/pdf")

        assert res.status_code == 200
        body = res.json()
        assert body["status"] == "success"

    def test_download_pdf_not_found(self, client: TestClient):
        folder = _create_project(client)
        res = client.get(f"/api/projects/{folder}/pdf/download")
        assert res.status_code == 404


# ---------------------------------------------------------------------------
# AI / Template
# ---------------------------------------------------------------------------

class TestAI:
    def test_get_template_default(self, client: TestClient):
        folder = _create_project(client)
        res = client.get(f"/api/projects/{folder}/template")
        assert res.status_code == 200
        template = res.json()["template"]
        assert "sections" in template

    def test_generate_existing_template(self, client: TestClient):
        folder = _create_project(client)
        res = client.post(
            f"/api/projects/{folder}/generate",
            json={"type": "existing"},
        )
        assert res.status_code == 200
        assert res.json()["type"] == "existing"

    def test_generate_ai_requires_assignment(self, client: TestClient):
        folder = _create_project(client)
        res = client.post(
            f"/api/projects/{folder}/generate",
            json={"type": "ai"},  # no assignment field
        )
        assert res.status_code == 422

    def test_generate_ai_template(self, client: TestClient):
        folder = _create_project(client)

        fake_template = {"title": "AI Work", "sections": [{"name": "Intro", "blocks": []}]}

        with patch("api.services.ai_service.TemplateGenerator.generate_ai_template") as mock_gen:
            mock_gen.return_value = fake_template

            res = client.post(
                f"/api/projects/{folder}/generate",
                json={"type": "ai", "assignment": "Faça um trabalho sobre IA."},
            )

        assert res.status_code == 200
        body = res.json()
        assert body["type"] == "ai_generated"
        assert body["template"]["title"] == "AI Work"

    def test_list_assignments(self, client: TestClient):
        from academic_manager.config.settings import Config
        (Config.ASSIGNMENTS_DIR / "trabalho1.md").write_text("Enunciado 1", encoding="utf-8")

        res = client.get("/api/assignments")
        assert res.status_code == 200
        assignments = res.json()["assignments"]
        assert "trabalho1.md" in assignments
