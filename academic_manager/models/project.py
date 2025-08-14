from dataclasses import dataclass, asdict
from typing import Dict, Optional
from pathlib import Path


@dataclass
class ProjectMetadata:
    curso: str
    aluno: str
    titulo: str
    local: str
    ano: int
    disciplina: str
    orientador: str

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'ProjectMetadata':
        return cls(**data)


@dataclass
class Project:
    name: str
    path: Path
    metadata: ProjectMetadata
    template: Optional[Dict] = None