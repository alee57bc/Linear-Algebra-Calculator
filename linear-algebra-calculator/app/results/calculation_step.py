from dataclasses import dataclass
from typing import Any

@dataclass
class CalculationStep:
    description: str
    result: Any