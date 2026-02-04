import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

load_dotenv(".env")

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PWD = os.getenv("NEO4J_PASSWORD")
DB = os.getenv("NEO4J_DATABASE", "neo4j")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

chunks = [
    ("c1", "Squats strengthen the quadriceps, glutes, and hamstrings."),
    ("c2", "Keep knees aligned with toes and maintain a neutral spine during squats."),
    ("c3", "Stop if you feel sharp pain, dizziness, or joint instability."),
]

with GraphDatabase.driver(URI, auth=(USER, PWD)) as driver:
    for cid, text in chunks:
        emb = model.encode(text).tolist()  # 384 floats
        driver.execute_query(
            """
            MERGE (c:Chunk {id: $id})
            SET c.text = $text,
                c.embedding = $embedding
            """,
            id=cid,
            text=text,
            embedding=emb,
            database_=DB,
        )

print("Seeded demo chunks with embeddings.")