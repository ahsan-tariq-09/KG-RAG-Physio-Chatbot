import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from google import genai

load_dotenv()

# ---------- CONFIG ----------
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD]):
    raise RuntimeError("Missing Neo4j credentials in .env")

if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY")

# ---------- 1️⃣ Query Neo4j ----------
driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

query = """
MATCH (c:Condition)
WHERE toLower(c.name) CONTAINS 'back'
MATCH (a:Article)-[:ADDRESSES_CONDITION]->(c)
OPTIONAL MATCH (a)-[:DESCRIBES_EXERCISE]->(e:Exercise)
RETURN a.title AS title,
       collect(DISTINCT c.name)[0..3] AS conditions,
       collect(DISTINCT e.name)[0..5] AS exercises
LIMIT 3
"""

with driver.session(database="neo4j") as session:
    records = session.run(query)
    kg_results = [r.data() for r in records]

driver.close()

print("KG Results:")
print(kg_results)

# ---------- 2️⃣ Send KG Evidence to Gemini ----------
client = genai.Client(api_key=GEMINI_API_KEY)

prompt = f"""
Use ONLY the following knowledge graph evidence to answer:

{kg_results}

Explain what exercises help back pain and why.
"""

resp = client.models.generate_content(
    model=MODEL,
    contents=prompt,
)

print("\nGemini Response:")
print(resp.text)