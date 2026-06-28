from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    chunk_size: int = 900
    chunk_overlap: int = 150
    top_k: int = 10

    embedding_model: str = "BAAI/bge-small-en-v1.5"
    ollama_model: str = "llama3.2"

    vector_db_path: str = "data/vectordb"
    document_path: str = "data/documents"

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()