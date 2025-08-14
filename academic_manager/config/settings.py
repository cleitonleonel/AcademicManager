import os
from datetime import datetime
from pathlib import Path
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

os.environ["API_KEY"] = config["DEFAULT"]["api_key"]

API_KEY = os.environ["API_KEY"]


class Config:
    """
    Configuration for academic projects.

    This class provides the default configuration for academic project directories,
    metadata, templates, and instructions. It defines the structure and values
    for essential elements required to set up and manage academic projects.
    """
    BASE_DIR = Path("academic_projects")
    ASSIGNMENTS_DIR = BASE_DIR / "assignments"
    ENABLE_DOWNLOADS = config["DEFAULT"].getboolean("enable_downloads")

    DEFAULT_METADATA = {
        "curso": "[NOME DO CURSO AQUI]",
        "aluno": "[NOME DO ALUNO AQUI]",
        "titulo": "[TÍTULO DO TRABALHO AQUI]",
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
