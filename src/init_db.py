import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # dossier /src
DB_PATH = os.path.join(BASE_DIR, "..", "database", "store.db")

# Charger le schema
with open(os.path.join(BASE_DIR, "..", "database", "schema.sql"), "r", encoding="utf-8") as f:
    schema = f.read()

# Charger les données initiales
with open(os.path.join(BASE_DIR, "..", "database", "seed.sql"), "r", encoding="utf-8") as f:
    seed = f.read()

# Créer la base
conn = sqlite3.connect(DB_PATH)
conn.executescript(schema)
conn.executescript(seed)
conn.commit()
conn.close()

print("Base de données initialisée avec succès.")
