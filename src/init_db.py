import sqlite3

with open("../database/schema.sql", "r", encoding="utf-8") as f:
    schema = f.read()

conn = sqlite3.connect("store.db")
conn.executescript(schema)
conn.commit()
conn.close()

print("Base de données initialisée avec succès.")
