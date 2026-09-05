from dataclasses import dataclass, field
from typing import Any


@dataclass
class HistoryEntry:
    operation: str
    inputs: list[Any]
    result: Any
    steps: list = field(default_factory=list)
    extra_results: list = field(default_factory=list)