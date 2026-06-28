from sentence_transformers import SentenceTransformer

from config import settings
from .embedding import Embedding


class Embedder:

    def __init__(self):

        self.model = SentenceTransformer(
            settings.embedding_model
        )

    @property
    def model_name(self):

        return settings.embedding_model

    @property
    def dimension(self):

        return self.model.get_sentence_embedding_dimension()

    def embed_chunks(self, chunks):

        texts = [chunk.text for chunk in chunks]

        vectors = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
        )

        embeddings = []

        for chunk, vector in zip(chunks, vectors):

            embeddings.append(
                Embedding(
                    chunk_id=chunk.id,
                    vector=vector.tolist(),
                    metadata=chunk.metadata,
                    text=chunk.text,
                )
            )

        return embeddings
    

    def embed_query(self, query: str):

        vector = self.model.encode(
            query,
            convert_to_numpy=True,
        )

        return vector.tolist()