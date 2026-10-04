
import sqlite3
import hashlib
from pathlib import Path

from database import get_connection


# ---------------------------------------------------------
# CALCULATE SHA-256 HASH
# ---------------------------------------------------------
def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""

    base_dir = Path(__file__).resolve().parent.parent
    path = Path(file_path)

    if not path.is_absolute():
        path = base_dir / path

    if not path.is_file():
        raise FileNotFoundError(
            f"Model artifact not found: {path}"
        )

    sha256 = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


# ---------------------------------------------------------
# REGISTER ARTIFACT HASH
# ---------------------------------------------------------
def store_artifact_hash(model_version):
    """Calculate and store the hash for a registered model."""

    connection = get_connection()

    try:
        artifact = connection.execute(
            """
            SELECT artifact_path
            FROM model_artifacts
            WHERE model_version = ?
            """,
            (model_version,)
        ).fetchone()

        if artifact is None:
            return False, "Model version not found."

        artifact_path = artifact["artifact_path"]

        if not artifact_path:
            return False, "No artifact path is registered."

        artifact_hash = calculate_sha256(artifact_path)

        connection.execute(
            """
            UPDATE model_artifacts
            SET artifact_hash = ?,
                hash_verified_at = NULL
            WHERE model_version = ?
            """,
            (artifact_hash, model_version)
        )

        connection.commit()
        return True, artifact_hash

    except (OSError, sqlite3.Error, ValueError) as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()


# ---------------------------------------------------------
# VERIFY ARTIFACT INTEGRITY
# ---------------------------------------------------------
def verify_artifact_hash(model_version):
    """Compare the current artifact hash with its stored hash."""

    connection = get_connection()

    try:
        artifact = connection.execute(
            """
            SELECT artifact_path, artifact_hash
            FROM model_artifacts
            WHERE model_version = ?
            """,
            (model_version,)
        ).fetchone()

        if artifact is None:
            return False, "Model version not found."

        artifact_path = artifact["artifact_path"]
        stored_hash = artifact["artifact_hash"]

        if not artifact_path:
            return False, "No artifact path is registered."

        if not stored_hash:
            return False, "No SHA-256 hash is registered."

        current_hash = calculate_sha256(artifact_path)

        if current_hash != stored_hash:
            return False, "FAILED: Artifact integrity check failed."

        connection.execute(
            """
            UPDATE model_artifacts
            SET hash_verified_at = CURRENT_TIMESTAMP
            WHERE model_version = ?
            """,
            (model_version,)
        )

        connection.commit()
        return True, "REPRODUCIBLE: Artifact hash verified."

    except (OSError, sqlite3.Error, ValueError) as error:
        connection.rollback()
        return False, str(error)

    finally:
        connection.close()