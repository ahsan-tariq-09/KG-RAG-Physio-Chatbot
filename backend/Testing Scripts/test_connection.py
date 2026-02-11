from neo4j import GraphDatabase

URI = "neo4j+s://af6ca5a7.databases.neo4j.io"
AUTH = ("neo4j", "MnsOTZ_pYl6I0R8d1IHZuLOrAuH_KiFVvfNpE-YSeBc")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connection successful.")
