# **KG-RAG Physical Rehabilitation Chatbot**

## A Knowledge-Graph-Enhanced Retrieval-Augmented Generation (KG-RAG) system for explainable physical therapy queries

---

## **Overview**

This project implements the backend foundation of a **physical rehabilitation chatbot** based on **Knowledge-Graph-Enhanced Retrieval-Augmented Generation (KG-RAG)**.

Rather than relying solely on unstructured text retrieval, the system grounds its responses in a **Neo4j knowledge graph**, enabling **transparent, evidence-based answers** for rehabilitation and exercise-related questions.

The backend exposes a `/query` API that retrieves relevant graph-backed evidence and generates responses using a large language model.

---

## **Core Technologies**

The current implementation integrates:

- **Neo4j** — persistent storage for rehabilitation knowledge as a graph  
- **Neo4j GraphRAG** — graph-aware retrieval following Microsoft’s GraphRAG principles  
- **Sentence-Transformers (MiniLM)** — local open-source embeddings for semantic search  
- **FastAPI** — backend API layer  
- **Google Gemini (Flash models)** — LLM used to generate grounded answers  

A **Streamlit frontend** will be added to visualize retrieved subgraphs and improve interpretability.

---

## **Current Capabilities**

At its current stage, the project provides:

- A working **FastAPI backend**
- A `/query` endpoint that performs:
  - semantic retrieval over Neo4j vector indexes
  - graph-aware evidence aggregation
  - LLM answer generation grounded in retrieved evidence
- Structured responses containing:
  - an LLM-generated answer
  - retrieved text context
  - placeholders for graph nodes and edges (to be visualized in the frontend)

This implementation reflects the **backend architecture described in the project proposal** and serves as a stable research and development foundation.

---

## **Project Goal**

The primary goal of this project is to develop an **accurate, explainable, and research-driven chatbot** for physical rehabilitation.

Key objectives include:

- Reducing hallucinations by grounding answers in structured graph evidence  
- Improving transparency by exposing the reasoning context behind each response  
- Supporting future visualization of rehabilitation knowledge as interactive subgraphs  

---

## **Planned Extensions**

Future development phases will include:

- **Streamlit frontend** for interactive querying and graph visualization  
- **Subgraph visualization** using NetworkX and PyVis  
- **Multimodal extensions**, such as:
  - CLIP-based exercise image embeddings  
  - BLIP-2 image captioning  
- **Advanced retrieval strategies**, including FAISS-based similarity search  

---

## **Research Context**

This project aligns with contemporary research on **Graph-based Retrieval-Augmented Generation** and is designed to support exploratory academic research into **trustworthy and explainable AI systems** for healthcare and rehabilitation domains.

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
│   ├── .env.example               # Example env file (safe to commit)
│   ├── list_models.py             # Utility script to list Gemini models
│   
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
