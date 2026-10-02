import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "model_registry.db"

connection = sqlite3.connect(DB_PATH)

try:
    connection.execute("BEGIN")

    connection.execute("""
        CREATE TABLE feature_definitions_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_version TEXT NOT NULL,
            feature_name TEXT NOT NULL,
            definition TEXT NOT NULL,
            data_type TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(feature_version, feature_name)
        )
    """)

    connection.execute("""
        INSERT INTO feature_definitions_new
        (id, feature_version, feature_name, definition, data_type, created_at)
        SELECT
            id, 'feature_v1', feature_name,
            definition, data_type, created_at
        FROM feature_definitions
    """)

    connection.execute("DROP TABLE feature_definitions")

    connection.execute("""
        ALTER TABLE feature_definitions_new
        RENAME TO feature_definitions
    """)

    connection.commit()
    print("Feature table corrected successfully!")

    rows = connection.execute("""
        SELECT id, feature_version, feature_name
        FROM feature_definitions
        ORDER BY id
    """).fetchall()

    for row in rows:
        print(row)

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()