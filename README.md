# **KG-RAG Physical Rehabilitation Chatbot**

*A Knowledge-Graph-Enhanced Retrieval Augmented Generation System for Physical Therapy Queries*

This project implements the backend foundation of a rehabilitation-focused chatbot based on **Knowledge-Graph Retrieval-Augmented Generation (KG-RAG)**.
It integrates:

* **Neo4j** for the rehabilitation knowledge graph (built by collaborator)
* **Neo4j GraphRAG** for graph-aware retrieval following Microsoft’s GraphRAG principles
* **FastAPI** as the backend API layer
* **Gemini 3 Flash model** for generating answers grounded in retrieved graph evidence

The backend will later connect to a Streamlit frontend that visualizes subgraph evidence, enabling users to see how the system derived each answer.

The current stage focuses on backend architecture, Neo4j integration, GraphRAG scaffolding, and a working `/query` endpoint that returns:

* an LLM-generated answer
* an evidence subgraph (nodes + edges)
* retrieved text context

This is consistent with the system architecture described in the project proposal.

---

## **Project Goal**

The primary goal is to develop a chatbot that provides **accurate and explainable answers** to questions about physical rehabilitation exercises.
Instead of relying on plain text retrieval, the system grounds responses in **structured knowledge graph evidence**, reducing hallucinations and improving reasoning transparency.

This backend will serve as the foundation for later multimodal extensions such as CLIP embeddings, BLIP-2 captioning, FAISS similarity search, and Streamlit interface visualization.

---

## **Repository Structure**

```
KG-RAG-PHYSIO-CHATBOT/
│
├── backend/
│   ├── .venv/                     # Python virtual environment (local only)
│   │
│   ├── app/
│   │   ├── main.py                # FastAPI entrypoint (starts the backend API)
│   │   ├── config.py              # Environment variables & app configuration
│   │   ├── schemas.py             # Request/response data models (Pydantic)
│   │   │
│   │   └── services/
│   │       ├── neo4j_client.py    # Neo4j connection, driver, and queries
│   │       └── graphrag_service.py# GraphRAG pipeline (retrieval + Gemini)
│   │
│   ├── .env                       # Local secrets (NOT committed)
│   ├── .env.example               # Example env file (safe to commit)
│   ├── list_models.py             # Utility script to list Gemini models
│   ├── requirements.txt           # Backend dependencies
│
├── frontend/
│   ├── app.py                     # Streamlit frontend (graph + QA UI)
│   └── README.md                  # Frontend usage notes
│
├── tests/
│   ├── gemini_smoke_test.py       # Gemini API connectivity test
│   └── test_smoke.py              # Basic backend sanity tests
│
├── .gitignore                     # Files Git should ignore (.env, .venv, etc.)
├── LICENSE                        # Open-source license
├── README.md                      # Project overview & setup instructions
├── requirements.txt               # Combined frontend + backend dependencies
```
