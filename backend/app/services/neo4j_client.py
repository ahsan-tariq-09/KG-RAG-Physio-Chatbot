from neo4j import GraphDatabase, Driver


class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str, database: str | None = None):
        self._driver: Driver = GraphDatabase.driver(uri, auth=(user, password))
        self._database = database

    @property
    def driver(self) -> Driver:
        return self._driver

    def close(self) -> None:
        self._driver.close()
