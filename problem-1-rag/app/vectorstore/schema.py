from dataclasses import dataclass
from typing import List


@dataclass
class VectorRecord:
    chunk_id: str
    text: str
    vector: List[float]

    source: str
    file_type: str

    pages: int
    chunk_number: int

    embedding_model: str
    embedding_dimension: int