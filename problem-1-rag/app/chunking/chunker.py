import hashlib
import re
from typing import List

from config import settings

from .chunk import Chunk


class TextChunker:
    """
    Recursive text chunker that prefers paragraphs,
    then sentences, then words.
    """

    def __init__(
        self,
        chunk_size: int = settings.chunk_size,
        chunk_overlap: int = settings.chunk_overlap,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, document) -> List[Chunk]:

        text = self._clean(document.content)

        paragraphs = self._split_paragraphs(text)

        chunks = []

        chunk_number = 0

        for paragraph in paragraphs:

            paragraph_chunks = self._split_paragraph(paragraph)

            for chunk_text in paragraph_chunks:

                metadata = document.metadata.copy()
                metadata["chunk_number"] = chunk_number

                chunk_id = hashlib.sha256(
                    chunk_text.encode("utf-8")
                ).hexdigest()

                chunks.append(
                    Chunk(
                        id=chunk_id,
                        text=chunk_text,
                        metadata=metadata,
                    )
                )

                chunk_number += 1

        return chunks

    def _clean(self, text: str) -> str:

        text = re.sub(r"\r\n", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def _split_paragraphs(self, text: str):

        return [
            p.strip()
            for p in text.split("\n\n")
            if p.strip()
        ]

    def _split_paragraph(self, paragraph: str):

        if len(paragraph) <= self.chunk_size:
            return [paragraph]

        sentences = re.split(
            r"(?<=[.!?])\s+",
            paragraph,
        )

        chunks = []

        current = ""

        for sentence in sentences:

            if len(current) + len(sentence) < self.chunk_size:

                current += " " + sentence

            else:

                if current:

                    chunks.append(
                        current.strip()
                    )

                current = sentence

        if current:

            chunks.append(current.strip())

        return self._apply_overlap(chunks)

    def _apply_overlap(self, chunks):

        if len(chunks) <= 1:
            return chunks

        overlapped = []

        for i, chunk in enumerate(chunks):

            if i == 0:
                overlapped.append(chunk)
                continue

            previous = overlapped[-1]

            overlap = previous.split()

            overlap = overlap[
                -self.chunk_overlap :
            ]

            new_chunk = (
                " ".join(overlap)
                + " "
                + chunk
            )

            overlapped.append(new_chunk)

        return overlapped