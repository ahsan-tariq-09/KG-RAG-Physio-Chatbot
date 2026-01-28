from functools import lru_cache
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    # App
    app_name: str = "KG-RAG Physio (Gemini)"

    # Neo4j
    neo4j_uri: str = Field(default="bolt://localhost:7687")
    neo4j_user: str = Field(default="neo4j")
    neo4j_password: str = Field(default="password")
    neo4j_database: str | None = Field(default=None)  # optional

    # Gemini Developer API
    gemini_api_key: str = Field(default="")  
    gemini_model: str = Field(default="gemini-2.5-flash")

    # Retrieval
    vector_index_name: str = Field(default="rehab_vector_index")
    fulltext_index_name: str = Field(default="rehab_fulltext_index")  # optional (for hybrid)
    top_k: int = Field(default=5)


@lru_cache
def get_settings() -> Settings:
    return Settings(
        neo4j_uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        neo4j_user=os.getenv("NEO4J_USER", "neo4j"),
        neo4j_password=os.getenv("NEO4J_PASSWORD", "password"),
        neo4j_database=os.getenv("NEO4J_DATABASE") or None,
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        vector_index_name=os.getenv("VECTOR_INDEX_NAME", "rehab_vector_index"),
        fulltext_index_name=os.getenv("FULLTEXT_INDEX_NAME", "rehab_fulltext_index"),
        top_k=int(os.getenv("TOP_K", "5")),
    )
