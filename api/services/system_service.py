from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from academic_manager.config.settings import Config


def create_backup_zip() -> str:
    """
    Create a ZIP archive of the academic_projects directory.
    Returns the absolute path to the generated ZIP file.
    """
    # Root of what we want to backup
    source_dir = Config.BASE_DIR
    
    # Create temp directory for the zip
    temp_dir = Path(tempfile.gettempdir())
    zip_base_name = temp_dir / f"academic_manager_backup"
    
    # make_archive adds the extension automatically
    zip_path = shutil.make_archive(
        str(zip_base_name),
        "zip",
        root_dir=source_dir.parent,
        base_dir=source_dir.name
    )
    
    return zip_path


def restore_backup(zip_path: Path) -> bool:
    """
    Restore projects from a ZIP file by extracting it into the projects directory.
    Warning: This may overwrite existing files.
    """
    try:
        # Unpack to the parent of Config.BASE_DIR (usually the repo root)
        # since the zip contains the 'academic_projects' folder itself.
        shutil.unpack_archive(str(zip_path), Config.BASE_DIR.parent)
        return True
    except Exception:
        return False
