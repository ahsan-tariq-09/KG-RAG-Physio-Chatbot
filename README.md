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

- **Render frontend** for interactive querying and graph visualization (transition from StreamLit to Render) 
- **Subgraph visualization** using NetworkX and PyVis  
- **Multimodal extensions**, such as:
  - CLIP‑based static diagram embeddings 
- **Stack Improvement** : make Backend python code more optimised and A TypeScript + React frontend will be added to visualise retrieved subgraphs and supporting images

---

## **Research Context**

This project aligns with contemporary research on **Graph-based Retrieval-Augmented Generation** and is designed to support exploratory academic research into **trustworthy and explainable AI systems** for healthcare and rehabilitation domains.

---

## **Repository Structure**

```
KG-RAG-PHYSIO-CHATBOT/
│
├── backend/
│   ├── .venv/                          # Python virtual environment for local development
│   │
│   ├── app/
│   │   ├── main.py                     # FastAPI entry point
│   │   ├── config.py                   # Environment variables and app configuration
│   │   ├── schemas.py                  # Pydantic request/response schemas
│   │   │
│   │   └── services/
│   │       ├── neo4j_client.py         # Neo4j connection setup and graph queries
│   │       └── graphrag_service.py     # KG-RAG retrieval and Gemini response pipeline
│   │
│   ├── Testing Scripts/
│   │   ├── gemini_smoke_test.py        # Gemini API connectivity test
│   │   ├── list_models.py              # Utility to list available Gemini models
│   │   └── test_connection.py          # Neo4j / backend connection test
│   │
│   ├── .env.example                    # Example environment variables file
│   └── requirements.txt                # Backend Python dependencies
│
├── frontend/
│   ├── app.py                          # Streamlit frontend interface
│   └── README.md                       # Frontend usage notes
│
├── tests/
│   └── test_smoke.py                   # Basic backend smoke test(s)
│
├── .gitignore                          # Ignored files and folders (.env, .venv, caches, etc.)
├── progress screenshots                # Progress Photos
├── LICENSE                             # Open-source license
├── README.md                           # Project overview, setup, and usage instructions
└── requirements.txt                    # Combined project dependencies if kept at repo root
```
