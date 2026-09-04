from enum import Enum
from dataclasses import dataclass
from app.core.vector import Vector

class SolutionType(Enum):
    UNIQUE = "unique"
    NO_SOLUTION = "no_solution"
    INFINITE = "infinite"

@dataclass
class SystemSolution:
    solution_type: SolutionType
    solution: Vector | None = None