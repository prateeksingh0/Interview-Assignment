from dataclasses import dataclass
from typing import List


@dataclass
class GenerationResponse:
    answer: str
    latency: float