"""SQL queries for creating table and inserting data, meant for use in the first,
preliminary data exploration after web scraping."""

import sqlite3


def connect() -> sqlite3.Connection:
    return sqlite3.connect('cars.db')


def insert_table(conn, df, table_name: str) -> None:
    with conn:
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Inserted {len(df)} records into {table_name} table.")
