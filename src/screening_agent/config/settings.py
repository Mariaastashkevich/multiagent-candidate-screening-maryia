from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal


class Settings(BaseSettings):
    ENV: Literal["local", "dev", "prod"] = "local"

    LLM_PROVIDER: Literal["ollama", "openai"] = "ollama"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3:8b-instruct-q4"

    LLM_MAX_TOKENS: int = Field(default=512, ge=128, le=2048)
    LLM_TEMPERATURE: float = Field(default=0.2, ge=0.0, le=1.0)

    DB_URL: str
    DB_ECHO: bool = False

    VECTOR_STORE_TYPE: Literal["faiss", "chroma", "qdrant", "pgvector"] = "faiss"
    VECTOR_STORE_PATH: str = "./data/vectorstore"

    RAG_TOP_K: int = Field(default=5, ge=1, le=20)
    CHUNK_SIZE: int = Field(default=500, ge=200, le=1000)
    CHUNK_OVERLAP: int = Field(default=50, ge=0, le=200)

    ENABLE_RERANK: bool = True
    ENABLE_CHAT_MEMORY: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()



