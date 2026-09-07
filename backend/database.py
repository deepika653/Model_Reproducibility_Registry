import sqlite3
from pathlib import Path

# Always use the database in the main Model_Registry folder
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE = BASE_DIR / "model_registry.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_database():
    connection = get_connection()

    # ---------------------------------------------------------
    # 1. Dataset Versions
    # ---------------------------------------------------------
    connection.execute("""
        CREATE TABLE IF NOT EXISTS dataset_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_version TEXT UNIQUE NOT NULL,
            dataset_name TEXT NOT NULL,
            file_path TEXT,
            record_count INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---------------------------------------------------------
    # 2. Feature Definitions
    # ---------------------------------------------------------
    connection.execute("""
        CREATE TABLE IF NOT EXISTS feature_definitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_version TEXT UNIQUE NOT NULL,
            feature_name TEXT NOT NULL,
            definition TEXT NOT NULL,
            data_type TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---------------------------------------------------------
    # 3. Code Versions / Git Commits
    # ---------------------------------------------------------
    connection.execute("""
        CREATE TABLE IF NOT EXISTS code_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code_version TEXT UNIQUE NOT NULL,
            commit_hash TEXT NOT NULL,
            repository TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---------------------------------------------------------
    # 4. Model Artifacts
    # ---------------------------------------------------------
    connection.execute("""
        CREATE TABLE IF NOT EXISTS model_artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_version TEXT UNIQUE NOT NULL,
            model_name TEXT NOT NULL,
            artifact_path TEXT,
            algorithm TEXT,
            parameters TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---------------------------------------------------------
    # 5. Approvals
    # ---------------------------------------------------------
    connection.execute("""
        CREATE TABLE IF NOT EXISTS approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_version TEXT NOT NULL,
            approved_by TEXT NOT NULL,
            role TEXT NOT NULL,
            approval_status TEXT NOT NULL,
            approval_date TEXT DEFAULT CURRENT_TIMESTAMP,
            comments TEXT
        )
    """)

    # ---------------------------------------------------------
    # 6. Deployment Records
    # ---------------------------------------------------------
    connection.execute("""
        CREATE TABLE IF NOT EXISTS deployments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deployment_version TEXT UNIQUE NOT NULL,
            model_version TEXT NOT NULL,
            environment TEXT NOT NULL,
            deployed_by TEXT,
            deployment_status TEXT NOT NULL,
            deployment_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---------------------------------------------------------
    # 7. Historical Predictions
    # ---------------------------------------------------------
    connection.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            prediction TEXT NOT NULL,

            dataset_version TEXT,
            feature_version TEXT,
            code_version TEXT,
            model_version TEXT,
            deployment_version TEXT,

            parameters TEXT,

            reproducibility_status TEXT DEFAULT 'UNKNOWN',
            failure_reason TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---------------------------------------------------------
    # 8. Configurable Registry Rules
    # ---------------------------------------------------------
    connection.execute("""
        CREATE TABLE IF NOT EXISTS registry_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT UNIQUE NOT NULL,
            rule_description TEXT NOT NULL,
            rule_value TEXT NOT NULL,
            enabled INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_database()
    print("Model Reproducibility Registry database initialized successfully!")
    print(f"Database location: {DATABASE}")