"""
Project service — thin adapter between the FastAPI layer and the
academic_manager core (ProjectManager, FileManager, Config).
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from academic_manager.config.settings import Config
from academic_manager.core.file_manager import FileManager
from academic_manager.core.project_manager import ProjectManager


def _load_settings(project_id: str) -> Optional[Dict[str, Any]]:
    """Load settings.json for a given project folder.  Returns None if absent."""
    settings_path = Config.BASE_DIR / project_id / "settings.json"
    if not settings_path.exists():
        return None
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def _determine_status(project_path: Path, disciplina: str) -> str:
    """Derive a simple lifecycle status from the files present in a project dir."""
    if not project_path.exists():
        return "draft"

    files = list(project_path.iterdir())
    titulo_json_exists = any(f.suffix == ".json" and f.stem != "settings" for f in files)
    pdf_exists = any(f.suffix == ".pdf" for f in files)

    if pdf_exists:
        return "completed"
    if titulo_json_exists:
        return "progress"
    return "draft"


def _count_project_pdfs(project_id: str) -> int:
    """Count generated PDFs inside a project directory."""
    project_path = Config.BASE_DIR / project_id
    if not project_path.exists():
        return 0
    return sum(1 for f in project_path.iterdir() if f.suffix == ".pdf")


# ---------------------------------------------------------------------------
# Public service functions (all sync — called via asyncio.to_thread in routes)
# ---------------------------------------------------------------------------

def list_projects() -> List[Dict[str, Any]]:
    """Return all projects with summarised metadata."""
    FileManager.ensure_directories_exist()
    results = []

    for folder in FileManager.list_projects():
        settings = _load_settings(folder)
        if not settings:
            continue

        project_path = Config.BASE_DIR / folder
        status = _determine_status(project_path, settings.get("disciplina", ""))

        results.append(
            {
                "id": folder,
                "title": settings.get("titulo", "Projeto sem título"),
                "description": (
                    f"{settings.get('curso', '')} — {settings.get('disciplina', '')}"
                ),
                "author": settings.get("aluno", ""),
                "status": status,
                "type": settings.get("tipo", "").lower(),
                "created_date": settings.get("created_date", ""),
                "updated_date": settings.get("updated_date", ""),
                "edit_count": settings.get("edit_count", 0),
                "folder": folder,
            }
        )

    return results


def get_stats() -> Dict[str, int]:
    """Aggregate counters for the dashboard."""
    FileManager.ensure_directories_exist()
    projects = list_projects()
    active = len(projects)
    in_progress = sum(1 for p in projects if p["status"] == "progress")
    pdfs = sum(_count_project_pdfs(p["id"]) for p in projects)
    total_files = sum(
        len(FileManager.list_attachments(p["id"])) for p in projects
    )
    return {
        "active_projects": active,
        "generated_pdfs": pdfs,
        "in_progress": in_progress,
        "total_files": total_files,
    }


def get_project(project_id: str) -> Optional[Dict[str, Any]]:
    """Return raw settings dict for a project."""
    return _load_settings(project_id)


def create_project(data: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """
    Create the on-disk structure for a new project and return
    (project_folder_name, saved_metadata).
    """
    FileManager.ensure_directories_exist()

    # Build a safe folder name from the title
    titulo = data.get("titulo", "")
    folder_name = "".join(
        c for c in titulo if c.isalnum() or c in (" ", "-", "_")
    ).strip().replace(" ", "_") or f"project_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Avoid collisions
    base = folder_name
    counter = 1
    while (Config.BASE_DIR / folder_name).exists():
        folder_name = f"{base}_{counter}"
        counter += 1

    project_path = Config.BASE_DIR / folder_name

    pm = ProjectManager()
    pm._create_project_structure(project_path)

    metadata = {k: v for k, v in data.items() if k != "assignment"}
    metadata.setdefault("ano", datetime.now().year)
    metadata["created_date"] = datetime.now().isoformat()

    pm._save_project_files(project_path, metadata)

    # Save assignment if provided
    assignment = data.get("assignment")
    if assignment:
        assignments_path = Config.BASE_DIR / "assignments"
        pm._save_assignment_file(folder_name, assignments_path, assignment)

    return folder_name, metadata


def update_project(project_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update settings.json, renaming the template JSON if the title changed."""
    settings = _load_settings(project_id)
    if settings is None:
        return None

    project_path = Config.BASE_DIR / project_id

    # Rename template JSON if titulo changed
    old_title = settings.get("titulo", "")
    new_title = data.get("titulo", old_title)
    if old_title != new_title:
        old_stem = old_title.replace(" ", "_").capitalize()
        new_stem = new_title.replace(" ", "_").capitalize()
        old_json = project_path / f"{old_stem}.json"
        new_json = project_path / f"{new_stem}.json"
        if old_json.exists():
            old_json.rename(new_json)

    updated = {**settings, **{k: v for k, v in data.items() if k != "assignment"}}
    updated["updated_date"] = datetime.now().isoformat()
    updated["edit_count"] = settings.get("edit_count", 0) + 1
    
    pm = ProjectManager()
    pm._save_project_files(project_path, updated)

    return updated


def delete_project(project_id: str) -> bool:
    """Delete a project directory.  Returns False if it doesn't exist."""
    project_path = Config.BASE_DIR / project_id
    if not project_path.exists():
        return False
    shutil.rmtree(project_path)
    return True


def list_project_files(project_id: str) -> Optional[List[Dict[str, Any]]]:
    """List files (flat) within a project directory."""
    project_path = Config.BASE_DIR / project_id
    if not project_path.exists():
        return None

    files = []
    for fp in sorted(project_path.rglob("*")):
        if fp.is_file():
            stat = fp.stat()
            files.append(
                {
                    "name": fp.name,
                    "relative_path": str(fp.relative_to(project_path)),
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "type": fp.suffix.lstrip(".") or "unknown",
                }
            )
    return files


def save_attachment(project_id: str, filename: str, content: bytes) -> str:
    """Save an uploaded file to the project's attachments directory."""
    attachments_dir = Config.BASE_DIR / project_id / "attachments"
    attachments_dir.mkdir(parents=True, exist_ok=True)
    dest = attachments_dir / filename
    dest.write_bytes(content)
    return str(dest)
