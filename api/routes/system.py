from __future__ import annotations

import os
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from academic_manager.config.settings import Config
from api.services import system_service as svc

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/defaults")
async def get_defaults():
    """
    Return server-side default settings (safe metadata).
    """
    return {
        "model": Config.MODEL,
        "has_api_key": bool(Config.API_KEY),
        "institution": Config.DEFAULT_METADATA.get("instituicao"),
        "unit": Config.DEFAULT_METADATA.get("unidade"),
        "base_dir": str(Config.BASE_DIR),
        "status": "success"
    }


@router.get("/backup")
async def download_backup(background_tasks: BackgroundTasks):
    """
    Generate and download a ZIP backup of all projects.
    """
    try:
        zip_path = svc.create_backup_zip()
        
        # Ensure file is deleted after download
        background_tasks.add_task(lambda p: os.remove(p) if os.path.exists(p) else None, zip_path)
        
        return FileResponse(
            path=zip_path,
            filename="academic_manager_backup.zip",
            media_type="application/zip"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar backup: {str(e)}"
        )


@router.post("/restore")
async def restore_backup(file: UploadFile = File(...)):
    """
    Upload a ZIP backup and restore the projects directory.
    """
    if not file.filename.endswith(".zip"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo deve ser um formato .zip válido."
        )
    
    # Save temporary file for processing
    temp_zip = Path(f"temp_restore_{os.urandom(4).hex()}.zip")
    try:
        content = await file.read()
        with open(temp_zip, "wb") as f:
            f.write(content)
        
        success = svc.restore_backup(temp_zip)
        
        if not success:
            raise Exception("Falha na descompactação do arquivo.")
            
        return {"message": "Backup restaurado com sucesso", "status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao restaurar backup: {str(e)}"
        )
    finally:
        if temp_zip.exists():
            os.remove(temp_zip)
