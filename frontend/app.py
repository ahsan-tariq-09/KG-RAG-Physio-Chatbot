# starter version

import streamlit as st
import requests
import streamlit.components.v1 as components
from pyvis.network import Network

API_URL = "http://127.0.0.1:8000/query"

st.title("KG-RAG Physio Chatbot")

q = st.text_input("Ask a rehab question", "What muscles does a squat strengthen?")

if st.button("Ask"):
    resp = requests.post(API_URL, json={"query": q, "mode": "vector"})
    resp.raise_for_status()
    data = resp.json()

    st.subheader("Answer")
    st.write(data.get("answer", ""))

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    st.subheader("Evidence Graph")

    if not nodes:
        st.info("No graph returned yet. Backend must return nodes/edges.")
    else:
        net = Network(height="600px", width="100%", directed=True)
        net.toggle_physics(True)

        for n in nodes:
            net.add_node(
                n["id"],
                label=n.get("label", n["id"]),
                title=f'Type: {n.get("type","")}',
            )

        for e in edges:
            net.add_edge(
                e["source"],
                e["target"],
                label=e.get("relation", ""),
            )

        html = net.generate_html()
        components.html(html, height=650, scrolling=True)
