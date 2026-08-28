import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "csv"
DB_PATH = BASE_DIR / "data" / "animal_health.db"

def get_connection():
    """Create and return a SQLite database connection."""
    return sqlite3.connect(DB_PATH)

def load_csv_to_db(csv_file: str, table_name: str) -> None:
    """
    Load a CSV file into a SQLite table.

    Args:
        csv_file: Name of the CSV file inside data/csv/
        table_name: SQLite table name
    """

    csv_path = DATA_DIR / csv_file

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    df = df.drop_duplicates()

    with get_connection() as conn:
        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

    print(
        f"Loaded {len(df)} rows "
        f"into '{table_name}'"
    )


def initialize_database():
    """Load all CSV datasets into SQLite."""

    datasets = {
        "datafile.csv": "datafile",
        "INCIDENCE_OF_LIVESTOCK_DISEASES_IN_INDIA.csv": "disease_incidence",
        "Maharashtra_Villagewise_20th_Livestock_Poultry_Census.csv": "livestock_census",
        "Table-10.2-All-India_Livestock_and_Fisheries.csv": "livestock_fisheries",
    }

    for csv_file, table_name in datasets.items():
        load_csv_to_db(csv_file, table_name)


if __name__ == "__main__":
    initialize_database()