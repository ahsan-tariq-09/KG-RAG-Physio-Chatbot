import os
import streamlit as st
import requests
import streamlit.components.v1 as components
from pyvis.network import Network

# -----------------------------
# Config
# -----------------------------
st.set_page_config(page_title="KG-RAG Physio", layout="wide")

# Prefer secrets, then env var, else localhost fallback
API_URL = (
    st.secrets.get("API_URL", None)
    if hasattr(st, "secrets")
    else None
) or os.getenv("API_URL", "http://127.0.0.1:8000/query")

# -----------------------------
# CSS
# -----------------------------
st.markdown(
    """
<style>
/* Overall page background */
[data-testid="stAppViewContainer"] { background: #0b0f19; }

/* Hide default Streamlit menu/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Title */
.kg-title { font-size: 28px; font-weight: 800; color: #e8eefc; margin-bottom: 0.25rem; }
.kg-subtitle { color: #a9b7d0; margin-top: 0; margin-bottom: 1rem; }

/* Panels */
.panel {
    background: #111827;
    border: 1px solid #1f2a44;
    border-radius: 18px;
    padding: 14px 14px 10px 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
.panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}
.panel-title { font-size: 16px; font-weight: 700; color: #e8eefc; }
.badge {
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(59,130,246,0.25);
    color: #93c5fd;
    font-size: 12px;
}

/* Chat bubbles */
.bubble {
    max-width: 92%;
    padding: 10px 12px;
    border-radius: 14px;
    margin-bottom: 10px;
    line-height: 1.35;
    font-size: 14px;
    white-space: pre-wrap;
}
.user {
    margin-left: auto;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.25);
    color: #e8eefc;
}
.assistant {
    margin-right: auto;
    background: rgba(148,163,184,0.10);
    border: 1px solid rgba(148,163,184,0.20);
    color: #e8eefc;
}

/* Typing animation */
.typing { display: inline-flex; gap: 6px; align-items: center; }
.dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #93c5fd; opacity: 0.4;
    animation: pulse 1.2s infinite;
}
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes pulse {
  0%, 100% { transform: translateY(0); opacity: 0.35; }
  50% { transform: translateY(-3px); opacity: 1; }
}

/* Inputs */
.stTextInput > div > div > input {
    background: #0f172a !important;
    border: 1px solid #22304d !important;
    color: #e8eefc !important;
    border-radius: 12px !important;
}
.stButton > button {
    background: #2563eb !important;
    color: #fff !important;
    border: 1px solid #1d4ed8 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 8px 14px !important;
}
.stButton > button:hover { background: #1d4ed8 !important; }

/* Small text */
.muted { color: #a9b7d0; font-size: 12px; }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_nodes" not in st.session_state:
    st.session_state.last_nodes = []
if "last_edges" not in st.session_state:
    st.session_state.last_edges = []
if "last_mode" not in st.session_state:
    st.session_state.last_mode = "vector"

# -----------------------------
# Header (REMOVED Gemini)
# -----------------------------
st.markdown('<div class="kg-title">KG-RAG Physio</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="kg-subtitle">Ask rehab questions. Get an answer + evidence graph.</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# Layout: Chat (left) + Graph (right)
# -----------------------------
left, right = st.columns([2, 3], gap="large")

with left:
    # Panel wrapper (open)
    st.markdown(
        """
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">Chat</div>
            <div class="badge">RAG + Neo4j</div>
          </div>
        """,
        unsafe_allow_html=True,
    )

    # ✅ Use a Streamlit container for chat history (scrolls naturally)
    chat_box = st.container(height=520)

    with chat_box:
        for msg in st.session_state.messages:
            role = msg.get("role", "assistant")
            text = msg.get("text", "")
            bubble_class = "user" if role == "user" else "assistant"
            st.markdown(
                f'<div class="bubble {bubble_class}">{text}</div>',
                unsafe_allow_html=True,
            )

    # Controls BELOW chat (always clickable)
    mode = st.selectbox(
        "Retrieval mode",
        ["vector", "hybrid"],
        index=0 if st.session_state.last_mode == "vector" else 1,
    )
    st.session_state.last_mode = mode

    q = st.text_input(
        "Ask a rehab question",
        value="What muscles does a squat strengthen?",
        key="query_input",
    )

    colA, colB = st.columns([1, 1])
    ask = colA.button("Ask", use_container_width=True)
    clear = colB.button("Clear chat", use_container_width=True)

    if clear:
        st.session_state.messages = []
        st.session_state.last_nodes = []
        st.session_state.last_edges = []
        st.rerun()

    if ask and q.strip():
        st.session_state.messages.append({"role": "user", "text": q.strip()})

        # typing animation
        typing_placeholder = chat_box.empty()
        typing_placeholder.markdown(
            """
            <div class="bubble assistant">
              <div class="typing">
                <div class="dot"></div><div class="dot"></div><div class="dot"></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            resp = requests.post(API_URL, json={"query": q.strip(), "mode": mode}, timeout=60)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            typing_placeholder.empty()
            st.session_state.messages.append(
                {"role": "assistant", "text": f"⚠️ Backend request failed.\n\n**API_URL:** `{API_URL}`\n\n**Error:** {e}"}
            )
            st.rerun()

        typing_placeholder.empty()

        answer = data.get("answer", "")
        nodes = data.get("nodes", [])
        edges = data.get("edges", [])

        st.session_state.last_nodes = nodes
        st.session_state.last_edges = edges
        st.session_state.messages.append({"role": "assistant", "text": answer})
        st.rerun()

    st.markdown(f'<div class="muted">API_URL: <code>{API_URL}</code></div></div>', unsafe_allow_html=True)

with right:
    st.markdown(
        """
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">Evidence Graph</div>
            <div class="badge">pyvis</div>
          </div>
        """,
        unsafe_allow_html=True,
    )

    nodes = st.session_state.last_nodes
    edges = st.session_state.last_edges

    if not nodes:
        st.info("No graph returned yet. Ask a question after your backend returns nodes/edges.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        net = Network(height="650px", width="100%", directed=True, bgcolor="#111827", font_color="#e8eefc")
        net.toggle_physics(True)

        for n in nodes:
            net.add_node(
                n["id"],
                label=n.get("label", n["id"]),
                title=f'Type: {n.get("type", "")}',
            )

        for e in edges:
            net.add_edge(
                e["source"],
                e["target"],
                label=e.get("relation", ""),
            )

        html = net.generate_html()
        components.html(html, height=700, scrolling=True)
        st.markdown("</div>", unsafe_allow_html=True)