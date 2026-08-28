from langchain_community.utilities import SQLDatabase

DB_PATH = "animal_health.db"


def get_db() -> SQLDatabase:
    return SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")