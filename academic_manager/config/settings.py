from datetime import datetime
from pathlib import Path
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")


class Config:
    """
    Configuration for academic projects.

    This class provides the default configuration for academic project directories,
    metadata, templates, and instructions. It defines the structure and values
    for essential elements required to set up and manage academic projects.
    """
    BASE_DIR = Path("academic_projects")
    ASSIGNMENTS_DIR = BASE_DIR / "assignments"
    API_KEY = config["DEFAULT"]["api_key"]
    MODEL = config["DEFAULT"]["model"]
    FALLBACK_MODEL = config["DEFAULT"]["fallback_model"]
    ENABLE_DOWNLOADS = config["DEFAULT"].getboolean("enable_downloads")
    IGNORE_MASKS = config["DEFAULT"].getboolean("ignore_masks")
    IGNORE_LOGO = config["DEFAULT"].getboolean("ignore_logo")
    IGNORE_IMGS = config["DEFAULT"].getboolean("ignore_images")
    PDF_FONT = config["DEFAULT"].get("pdf_font", "LiberationSans")
    PDF_FONT_DIR = Path(config["DEFAULT"].get(
        "pdf_font_dir",
        "/usr/share/fonts/truetype/liberation2"
    ))
    PDF_FONT_SIZE = config["DEFAULT"].getint("pdf_font_size", 12)

    DEFAULT_METADATA = {
        "instituicao": "FUNDAÇÃO DE ASSISTÊNCIA E EDUCAÇÃO",
        "unidade": "CENTRO UNIVERSITÁRIO ESPÍRITO-SANTENSE",
        "tipo": "GRADUAÇÃO",
        "curso": "[NOME DO CURSO AQUI]",
        "aluno": "[NOME DO ALUNO AQUI]",
        "titulo": "[TÍTULO DO TRABALHO AQUI]",
        "subtitulo": "",
        "local": "[SUA CIDADE AQUI]",
        "ano": datetime.now().year,
        "disciplina": "[DISCIPLINA AQUI]",
        "orientador": "[NOME DO ORIENTADOR AQUI]"
    }

    DEFAULT_TEMPLATE = {
        "sections": [
            {"name": "Introdução"},
            {"name": "Desenvolvimento"},
            {"name": "Conclusão"},
            {"name": "Referências"}
        ]
    }
