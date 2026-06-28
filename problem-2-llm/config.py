"""Configuration helpers for llm-judge-evaluation."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    app_env: str = os.getenv("APP_ENV", "development")
