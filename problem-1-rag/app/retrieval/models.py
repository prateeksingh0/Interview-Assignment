from dataclasses import dataclass
from typing import Dict
from pathlib import Path


@dataclass
class RetrievedChunk:
    chunk_id: str
    text: str
    distance: float
    metadata: Dict

    @property
    def citation(self) -> str:

        source = Path(
            self.metadata["source"]
        ).name

        return (
            f"[Chunk "
            f"{self.metadata['chunk_number']} | "
            f"{source}]"
        )