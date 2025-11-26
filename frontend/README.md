KG-RAG Physical Rehabilitation Chatbot

A Knowledge-Graph-Enhanced Retrieval Augmented Generation System for Physical Therapy Queries

This project implements the backend foundation of a rehabilitation-focused chatbot based on
Knowledge-Graph Retrieval-Augmented Generation (KG-RAG).
It combines:

Neo4j (physical rehabilitation knowledge graph built by collaborator)

Neo4j GraphRAG (graph-aware retrieval following Microsoft’s GraphRAG method)

FastAPI backend (query endpoint)

OpenAI GPT models (response generation grounded in retrieved graph context)

This backend will later connect to a Streamlit frontend that visualizes retrieved subgraphs and provides an interactive chat interface.

This repo currently includes:

Project skeleton

Core API structure

Neo4j integration

GraphRAG service scaffolding

Query endpoint returning:

LLM answer

Evidence subgraph (nodes + edges)

Retrieved text context

This matches the backend architecture described in the proposal.
The full multimodal pipeline (CLIP, BLIP-2, FAISS) will be added later.

Project Goal

To create a chatbot that answers physical rehabilitation questions using verifiable, structured evidence from a knowledge graph instead of relying purely on language-model guesses.

This addresses the issue of hallucinations in traditional RAG systems and demonstrates how semantic graph structure improves accuracy, transparency, and reasoning.

Repository Structure
kg-rag-physio/
  backend/
    app/
      main.py                # FastAPI entrypoint
      config.py              # Environment & settings
      schemas.py             # API models
      services/
        neo4j_client.py      # Neo4j connection + queries
        graphrag_service.py  # GraphRAG + LLM pipeline
    requirements.txt
  frontend/
    app.py                   # Streamlit UI (future)
  README.md
