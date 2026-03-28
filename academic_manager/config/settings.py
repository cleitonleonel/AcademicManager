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
    ENABLE_DOWNLOADS = config["DEFAULT"].getboolean("enable_downloads")
    IGNORE_MASKS = config["DEFAULT"].getboolean("ignore_masks")
    IGNORE_LOGO = config["DEFAULT"].getboolean("ignore_logo")
    IGNORE_IMGS = config["DEFAULT"].getboolean("ignore_images")

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

    DEFAULT_INSTRUCTIONS = """# Instruções do Trabalho
Descreva aqui as orientações detalhadas para a geração do trabalho acadêmico.
Inclua tópicos como objetivos, metodologia, referências obrigatórias e formato do texto.
"""
