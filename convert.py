import sqlite3
import pandas as pd

DB_PATH = "animal_health.db"

CSV_TABLE_MAP = {
    "data/csv/datafile.csv": "disease_by_species",
    "data/csv/INCIDENCE_OF_LIVESTOCK_DISEASES_IN_INDIA.csv": "national_incidence_2005_2011",
    "data/csv/Table-10.2-All-India_Livestock_and_Fisheries.csv": "national_incidence_2005_2015",
    "data/csv/Maharashtra_Villagewise_20th_Livestock_Poultry_Census.csv": "livestock_census",
}


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.str.strip()
        .str.replace(r"[^\w]+", "_", regex=True)
        .str.strip("_")
    )
    return df


def create_database():
    conn = sqlite3.connect(DB_PATH)

    for csv_path, table_name in CSV_TABLE_MAP.items():
        print(f"Loading {csv_path} -> {table_name}")
        df = pd.read_csv(csv_path)
        df = clean_columns(df)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"  {len(df)} rows, {len(df.columns)} columns")

    conn.close()
    print("Database created successfully")


if __name__ == "__main__":
    create_database()