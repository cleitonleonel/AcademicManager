"""
AI service — wraps TemplateGenerator and FileManager for async usage.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from academic_manager.config.settings import Config
from academic_manager.core.file_manager import FileManager
from academic_manager.core.template_generator import TemplateGenerator


def list_assignments() -> List[str]:
    """Return sorted list of available assignment file names."""
    return FileManager.list_assignments()


def get_assignment_content(assignment_filename: str) -> Optional[str]:
    """Read and return the content of an assignment file."""
    assignment_path = Config.ASSIGNMENTS_DIR / assignment_filename
    try:
        with open(assignment_path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def generate_ai_template(
    project_id: str,
    assignment_content: str,
    api_key_override: str = None
) -> Optional[Dict[str, Any]]:
    """
    Generate a JSON template via Gemini AI for the given project.

    Loads attachments from the project's ``attachments/`` directory and
    passes them as ``media_data`` to ``TemplateGenerator.generate_ai_template``.

    This function is **synchronous** — wrap with ``asyncio.to_thread()``
    when calling from an async route.
    """
    titulo = _get_project_titulo(project_id)
    stem = titulo.replace(" ", "_").capitalize() if titulo else "template"
    output_path = Config.BASE_DIR / project_id / f"{stem}.json"

    attachments = FileManager.list_attachments(project_id)
    media_data: Dict[str, str] = {}
    for idx, filename in enumerate(attachments):
        attachment_path = Config.BASE_DIR / project_id / "attachments" / filename
        media_data[f"imagem_{idx + 1}"] = str(attachment_path)

    return TemplateGenerator.generate_ai_template(
        assignment_content,
        media_data,
        output_path,
        project_id,
        api_key_override,
    )


def load_existing_template(project_id: str) -> Optional[Dict[str, Any]]:
    """
    Load a previously saved template JSON for the project, or return the
    default 4-section template if none exists yet.
    """
    project_path = Config.BASE_DIR / project_id
    titulo = _get_project_titulo(project_id)

    if titulo and project_path.exists():
        # Tenta a correspondência literal
        stem = titulo.replace(" ", "_").capitalize()
        template_path = project_path / f"{stem}.json"
        
        if template_path.exists():
            try:
                with open(template_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass

        # Autocorreção: caso o título tenha mudado mas o JSON não renomeou
        # Procura qualquer JSON que não seja settings.json
        try:
            for json_file in project_path.glob("*.json"):
                if json_file.name != "settings.json":
                    with open(json_file, "r", encoding="utf-8") as f:
                        return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    return Config.DEFAULT_TEMPLATE


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_project_titulo(project_id: str) -> Optional[str]:
    """Read only the 'titulo' field from a project's settings.json."""
    settings_path = Config.BASE_DIR / project_id / "settings.json"
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            return json.load(f).get("titulo")
    except (OSError, json.JSONDecodeError):
        return None
