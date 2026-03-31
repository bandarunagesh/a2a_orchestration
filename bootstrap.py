import psycopg2
from falkordb import FalkorDB
import os

# PostgreSQL connection
pg_conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    database=os.getenv("POSTGRES_DB", "unify_plus"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "password")
)
pg_cursor = pg_conn.cursor()

# Create tables and insert synthetic data
pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS unify_plus (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    value FLOAT,
    date DATE
);
""")

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS ngdp (
    id SERIAL PRIMARY KEY,
    country VARCHAR(255),
    gdp FLOAT,
    year INT
);
""")

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS manual_excels (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255),
    data JSONB
);
""")

# Insert synthetic data
pg_cursor.executemany("INSERT INTO unify_plus (name, value, date) VALUES (%s, %s, %s)", [
    ("Item1", 100.0, "2023-01-01"),
    ("Item2", 200.0, "2023-01-02"),
    # Add more
])

pg_cursor.executemany("INSERT INTO ngdp (country, gdp, year) VALUES (%s, %s, %s)", [
    ("USA", 21427700, 2022),
    ("China", 17963100, 2022),
    # Add more
])

pg_cursor.execute("INSERT INTO manual_excels (filename, data) VALUES (%s, %s)", [
    ("file1.xlsx", '{"sheet1": {"col1": "val1"}}')
])

pg_conn.commit()
pg_conn.close()

# FalkorDB connection
falkor = FalkorDB(host=os.getenv("FALKORDB_HOST", "localhost"), port=6379)
graph = falkor.select_graph("clinical_ontology")

# Seed with clinical ontology (example)
graph.query("""
CREATE (o:Ontology {name: 'Clinical Ontology'})
CREATE (br:BusinessRule {rule: 'Rule1'})
CREATE (ms:MetricStore {metric: 'Metric1'})
CREATE (o)-[:HAS]->(br)
CREATE (o)-[:HAS]->(ms)
""")

print("Bootstrap completed.")