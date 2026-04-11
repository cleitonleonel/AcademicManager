"""
PDF service — wraps PDFGenerator with async support.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from academic_manager.config.settings import Config
from academic_manager.core.pdf_generator import PDFGenerator


def _get_template(project_id: str, titulo: str) -> Optional[Dict[str, Any]]:
    """Load the saved template JSON for a project, or return the default template."""
    project_path = Config.BASE_DIR / project_id
    if not project_path.exists():
        return Config.DEFAULT_TEMPLATE

    # 1. Tenta a correspondência exata
    stem = titulo.replace(" ", "_").capitalize()
    template_path = project_path / f"{stem}.json"

    if template_path.exists():
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    # 2. Se falhar, busca qualquer .json no diretório que não seja settings.json
    try:
        for json_file in project_path.glob("*.json"):
            if json_file.name != "settings.json":
                with open(json_file, "r", encoding="utf-8") as f:
                    return json.load(f)
    except (json.JSONDecodeError, OSError):
        pass

    # 3. Se não houver template de jeito nenhum, retorna o fixo padrão
    return Config.DEFAULT_TEMPLATE


def generate_pdf(project_id: str, metadata: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> Optional[str]:
    """
    Generate a PDF for the given project using its saved template.
    Returns the absolute path of the PDF on success, None on failure.

    This function is sync — call via ``asyncio.to_thread()`` from async routes.
    """
    template = _get_template(project_id, metadata.get("titulo", ""))
    generator = PDFGenerator()
    success = generator.generate_pdf(project_id, metadata, template, options=options)

    if not success:
        return None

    stem = metadata["titulo"].replace(" ", "_").capitalize()
    pdf_path = Config.BASE_DIR / project_id / f"{stem}.pdf"
    return str(pdf_path) if pdf_path.exists() else None


def get_pdf_path(project_id: str, titulo: str) -> Optional[Path]:
    """Return the Path of an existing PDF file for a project, or None."""
    stem = titulo.replace(" ", "_").capitalize()
    pdf_path = Config.BASE_DIR / project_id / f"{stem}.pdf"
    return pdf_path if pdf_path.exists() else None
