from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Embedding:
    chunk_id: str
    vector: List[float]
    metadata: Dict
    text: str