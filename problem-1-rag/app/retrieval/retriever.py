from config import settings

from typing import List
from app.embeddings.embedder import Embedder
from app.vectorstore.lancedb_store import LanceDBStore

from .models import RetrievedChunk


class Retriever:

    def __init__(self):

        self.embedder = Embedder()

        self.store = LanceDBStore()

    def retrieve(
        self,
        question: str,
        top_k: int = settings.top_k,
    ) -> List[RetrievedChunk]:
        
        """
        Retrieve the top-k most relevant document chunks
        for a user question using vector similarity search.
        """

        query_vector = self.embedder.embed_query(
            question
        )

        results = self.store.search(
            query_vector,
            top_k,
        )

        retrieved = []

        for row in results:

            retrieved.append(

                RetrievedChunk(

                    chunk_id=row["chunk_id"],

                    text=row["text"],

                    distance=row["_distance"],

                    metadata={
                        "source": row["source"],
                        "file_type": row["file_type"],
                        "pages": row["pages"],
                        "chunk_number": row["chunk_number"],
                    },
                )

            )

        retrieved.sort(key=lambda chunk: chunk.distance)

        return retrieved