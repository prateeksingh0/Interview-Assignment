from pathlib import Path

import lancedb
import pyarrow as pa

from config import settings


class LanceDBStore:

    TABLE_NAME = "documents"

    def __init__(self):

        Path(settings.vector_db_path).mkdir(
            parents=True,
            exist_ok=True,
        )

        self.db = lancedb.connect(
            settings.vector_db_path
        )

        self.table = self._create_table()

    def _create_table(self):

        if self.TABLE_NAME in self.db.table_names():
            return self.db.open_table(
                self.TABLE_NAME
            )

        schema = pa.schema([
            pa.field("chunk_id", pa.string()),
            pa.field("text", pa.string()),
            pa.field("vector", pa.list_(pa.float32(), 384)),
            pa.field("source", pa.string()),
            pa.field("file_type", pa.string()),
            pa.field("pages", pa.int32()),
            pa.field("chunk_number", pa.int32()),
            pa.field("embedding_model", pa.string()),
            pa.field("embedding_dimension", pa.int32()),
        ])

        return self.db.create_table(
            self.TABLE_NAME,
            schema=schema,
        )

    def count(self):

        return self.table.count_rows()

    def all(self):
        return self.table.to_arrow().to_pylist()
    
    def get_existing_chunk_ids(self):

        if self.count() == 0:
            return set()

        table = self.table.to_arrow()

        return set(
            table.column("chunk_id").to_pylist()
        )
        
    def ingest(
        self,
        embeddings,
        model_name,
        dimension,
    ):

        existing_ids = self.get_existing_chunk_ids()

        records = []

        inserted = 0

        skipped = 0

        for embedding in embeddings:

            if embedding.chunk_id in existing_ids:
                skipped += 1
                continue

            metadata = embedding.metadata

            records.append(
                {
                    "chunk_id": embedding.chunk_id,
                    "text": embedding.text,
                    "vector": embedding.vector,
                    "source": metadata["source"],
                    "file_type": metadata["type"],
                    "pages": metadata.get("pages", 0),
                    "chunk_number": metadata["chunk_number"],
                    "embedding_model": model_name,
                    "embedding_dimension": dimension,
                }
            )

            inserted += 1

        if records:
            self.table.add(records)

        return {
            "inserted": inserted,
            "skipped": skipped,
            "total": self.count(),
        }
    
    def filter_by_source(
        self,
        source,
    ):

        return (
            self.table
            .search()
            .where(
                f"source = '{source}'",
                prefilter=True,
            )
            .limit(10000)
            .to_list()
        )
    
    def search(
        self,
        query_vector,
        top_k,
    ):

        return (
            self.table
            .search(query_vector)
            .limit(top_k)
            .to_list()
        )