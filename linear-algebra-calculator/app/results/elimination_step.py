from dataclasses import dataclass
from app.core.matrix import Matrix

@dataclass
class EliminationStep:
    description: str
    matrix: Matrix