from pydantic import BaseModel
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    # FastAPI
    app_name: str = "KG-RAG Physio Chatbot"

    # Neo4j (your collaborator’s rehab KG)
    neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "password")

    # OpenAI / GPT API
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # GraphRAG / retrieval
    index_name: str = os.getenv("GRAPH_INDEX_NAME", "rehab_index")


@lru_cache
def get_settings() -> Settings:
    return Settings()