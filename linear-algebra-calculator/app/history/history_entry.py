from dataclasses import dataclass
from typing import Any


@dataclass
class HistoryEntry:
    operation: str
    inputs: list[Any]
    result: Any