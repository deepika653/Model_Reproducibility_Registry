
from flask import Flask, jsonify, render_template
from pathlib import Path
from database import init_database, get_connection
import csv
import re


# ---------------------------------------------------------
# APPLICATION SETUP
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates")
)

init_database()


# ---------------------------------------------------------
# SHARED DATASET SCHEMA HELPERS
# ---------------------------------------------------------

def resolve_dataset_file(file_path):
    """Resolve a dataset file safely within the project directory."""
    root = BASE_DIR.resolve()
    path = (root / file_path).resolve()

    if not path.is_relative_to(root):
        raise ValueError("Dataset path is outside the project directory.")

    if not path.is_file():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    return path


def infer_column_type(values):
    """Infer a basic type from non-empty CSV values."""
    values = [
        str(value).strip()
        for value in values
        if value is not None and str(value).strip()
    ]

    if not values:
        return "unknown"

    try:
        for value in values:
            int(value)
        return "integer"
    except ValueError:
        pass

    try:
        for value in values:
            float(value)
        return "real"
    except ValueError:
        return "text"


def read_csv_schema(file_path):
    """Read CSV column names, inferred types, and nullability."""
    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file has no headers.")

        headers = reader.fieldnames

        if any(not name or not name.strip() for name in headers):
            raise ValueError("CSV contains an empty column name.")

        if len(headers) != len(set(headers)):
            raise ValueError("CSV contains duplicate column names.")

        values = {name: [] for name in headers}
        nullable = {name: False for name in headers}

        for row in reader:
            for name in headers:
                value = row.get(name)

                if value is None or not str(value).strip():
                    nullable[name] = True
                else:
                    values[name].append(value)

        return {
            name: {
                "data_type": infer_column_type(values[name]),
                "nullable": int(nullable[name])
            }
            for name in headers
        }


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.route("/")
def home():
    return "Model Reproducibility Registry is running!"


# ---------------------------------------------------------
# REGISTER DATASET
# ---------------------------------------------------------

@app.route("/register-dataset")
def register_dataset():
    connection = get_connection()

    try:
        connection.execute("""
            INSERT OR IGNORE INTO dataset_versions
            (dataset_version, dataset_name, file_path, record_count)
            VALUES (?, ?, ?, ?)
        """, (
            "dataset_v1",
            "Hospital Synthetic Risk Dataset",
            "data/dataset_v1.csv",
            5000
        ))

        connection.commit()
        return "dataset_v1 registered successfully!"

    finally:
        connection.close()


# ---------------------------------------------------------
# VIEW DATASETS
# ---------------------------------------------------------

@app.route("/datasets")
def get_datasets():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM dataset_versions
            ORDER BY id
        """).fetchall()

        return jsonify([dict(row) for row in rows])

    finally:
        connection.close()


# ---------------------------------------------------------
# REGISTER FEATURES
# ---------------------------------------------------------

@app.route("/register-features")
def register_features():
    connection = get_connection()

    features = [
        ("feature_v1", "age", "Patient age in years", "integer"),
        ("feature_v1", "gender", "Patient gender category", "categorical"),
        ("feature_v1", "blood_pressure",
         "Patient blood pressure measurement", "integer"),
        ("feature_v1", "glucose_level",
         "Patient glucose level measurement", "integer"),
        ("feature_v1", "heart_rate",
         "Patient heart rate measurement", "integer"),
        ("feature_v1", "symptom_score",
         "Patient symptom severity score from 0 to 10", "integer")
    ]

    try:
        connection.executemany("""
            INSERT OR IGNORE INTO feature_definitions
            (feature_version, feature_name, definition, data_type)
            VALUES (?, ?, ?, ?)
        """, features)

        connection.commit()
        return "Features registered successfully!"

    finally:
        connection.close()


# ---------------------------------------------------------
# VIEW FEATURES
# ---------------------------------------------------------

@app.route("/features")
def get_features():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM feature_definitions
            ORDER BY id
        """).fetchall()

        return jsonify([dict(row) for row in rows])

    finally:
        connection.close()


# ---------------------------------------------------------
# REGISTER CODE VERSION WITH FULL GIT SHA
# ---------------------------------------------------------

@app.route("/register-code")
def register_code():
    code_version = "code_v1"
    commit_hash = "66e5b85a064ec5e56dbcacca0716a418ab6ce1b5"
    repository = "Model_Reproducibility_Registry"

    if not re.fullmatch(r"[0-9a-fA-F]{40}", commit_hash):
        return jsonify({
            "status": "FAILED",
            "message": "Invalid full Git commit SHA"
        }), 400

    commit_hash = commit_hash.lower()
    connection = get_connection()

    try:
        existing = connection.execute("""
            SELECT commit_hash
            FROM code_versions
            WHERE code_version = ?
        """, (code_version,)).fetchone()

        if existing:
            stored_hash = (existing["commit_hash"] or "").lower()

            if commit_hash.startswith(stored_hash):
                connection.execute("""
                    UPDATE code_versions
                    SET commit_hash = ?
                    WHERE code_version = ?
                """, (commit_hash, code_version))

                connection.commit()

                return jsonify({
                    "status": "SUCCESS",
                    "message": "Code version updated with full SHA",
                    "code_version": code_version,
                    "commit_hash": commit_hash
                })

            if stored_hash != commit_hash:
                return jsonify({
                    "status": "FAILED",
                    "message": (
                        "Different commit already registered. "
                        "Use a new code version."
                    )
                }), 409

            return jsonify({
                "status": "SUCCESS",
                "message": "Code version already registered",
                "code_version": code_version,
                "commit_hash": commit_hash
            })

        connection.execute("""
            INSERT INTO code_versions
            (code_version, commit_hash, repository)
            VALUES (?, ?, ?)
        """, (code_version, commit_hash, repository))

        connection.commit()

        return jsonify({
            "status": "SUCCESS",
            "message": "Code version registered successfully",
            "code_version": code_version,
            "commit_hash": commit_hash
        })

    except Exception as error:
        connection.rollback()
        app.logger.exception("Code registration failed")
        return jsonify({
            "status": "FAILED",
            "message": str(error)
        }), 500

    finally:
        connection.close()


# ---------------------------------------------------------
# VIEW CODE VERSIONS
# ---------------------------------------------------------

@app.route("/code-versions")
def get_code_versions():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM code_versions
            ORDER BY id
        """).fetchall()

        return jsonify([dict(row) for row in rows])

    finally:
        connection.close()


# ---------------------------------------------------------
# REGISTER MODEL
# ---------------------------------------------------------

@app.route("/register-model")
def register_model():
    connection = get_connection()

    try:
        connection.execute("""
            INSERT OR IGNORE INTO model_artifacts
            (model_version, model_name, artifact_path,
             algorithm, parameters)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "model_v1",
            "Hospital Risk Prediction Model",
            "models/model_v1.pkl",
            "DecisionTreeClassifier",
            "max_depth=5, random_state=42, accuracy=98.8%"
        ))

        connection.commit()
        return "model_v1 registered successfully!"

    finally:
        connection.close()


# ---------------------------------------------------------
# VIEW MODELS
# ---------------------------------------------------------

@app.route("/models")
def get_models():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM model_artifacts
            ORDER BY id
        """).fetchall()

        return jsonify([dict(row) for row in rows])

    finally:
        connection.close()


# ---------------------------------------------------------
# REGISTER APPROVAL
# ---------------------------------------------------------

@app.route("/register-approval")
def register_approval():
    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO approvals
            (model_version, approved_by, role,
             approval_status, comments)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "model_v1",
            "Hospital Auditor",
            "Auditor",
            "APPROVED",
            "Model reviewed for reproducibility and audit tracking"
        ))

        connection.commit()
        return "Model approval registered successfully!"

    finally:
        connection.close()


# ---------------------------------------------------------
# VIEW APPROVALS
# ---------------------------------------------------------

@app.route("/approvals")
def get_approvals():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM approvals
            ORDER BY id
        """).fetchall()

        return jsonify([dict(row) for row in rows])

    finally:
        connection.close()


# ---------------------------------------------------------
# REGISTER DEPLOYMENT
# ---------------------------------------------------------

@app.route("/register-deployment")
def register_deployment():
    connection = get_connection()

    try:
        connection.execute("""
            INSERT OR IGNORE INTO deployments
            (deployment_version, model_version,
             environment, deployed_by, deployment_status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "deployment_v1",
            "model_v1",
            "Testing",
            "ML Engineer",
            "DEPLOYED"
        ))

        connection.commit()
        return "deployment_v1 registered successfully!"

    finally:
        connection.close()


# ---------------------------------------------------------
# VIEW DEPLOYMENTS
# ---------------------------------------------------------

@app.route("/deployments")
def get_deployments():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM deployments
            ORDER BY id
        """).fetchall()

        return jsonify([dict(row) for row in rows])

    finally:
        connection.close()


# ---------------------------------------------------------
# VIEW PREDICTIONS
# ---------------------------------------------------------

@app.route("/predictions")
def get_predictions():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM predictions
            ORDER BY id
        """).fetchall()

        return jsonify([dict(row) for row in rows])

    finally:
        connection.close()


# ---------------------------------------------------------
# REPRODUCIBILITY VALIDATION
# ---------------------------------------------------------

@app.route("/validate-reproducibility")
def validate_reproducibility():
    connection = get_connection()

    try:
        predictions = connection.execute("""
            SELECT *
            FROM predictions
            ORDER BY id
        """).fetchall()

        results = []

        for prediction in predictions:
            failure_reasons = []

            checks = [
                ("dataset_versions", "dataset_version",
                 prediction["dataset_version"], "Dataset version not found"),
                ("feature_definitions", "feature_version",
                 prediction["feature_version"], "Feature version not found"),
                ("code_versions", "code_version",
                 prediction["code_version"], "Code version not found"),
                ("model_artifacts", "model_version",
                 prediction["model_version"], "Model version not found")
            ]

            for table, column, value, message in checks:
                row = connection.execute(
                    f"SELECT 1 FROM {table} WHERE {column} = ?",
                    (value,)
                ).fetchone()

                if not row:
                    failure_reasons.append(message)

            status = "REPRODUCIBLE" if not failure_reasons else "FAILED"
            failure_reason = "; ".join(failure_reasons) or None

            connection.execute("""
                UPDATE predictions
                SET reproducibility_status = ?,
                    failure_reason = ?
                WHERE id = ?
            """, (
                status,
                failure_reason,
                prediction["id"]
            ))

            results.append({
                "prediction_id": prediction["id"],
                "patient_id": prediction["patient_id"],
                "status": status,
                "failure_reason": failure_reason
            })

        connection.commit()
        return jsonify(results)

    except Exception:
        connection.rollback()
        app.logger.exception("Reproducibility validation failed")
        raise

    finally:
        connection.close()


# ---------------------------------------------------------
# REPRODUCIBILITY EXPERIMENT
# ---------------------------------------------------------

@app.route("/reproducibility-experiment")
def reproducibility_experiment():
    connection = get_connection()

    try:
        total = connection.execute("""
            SELECT COUNT(*) FROM predictions
        """).fetchone()[0]

        reproducible = connection.execute("""
            SELECT COUNT(*)
            FROM predictions
            WHERE reproducibility_status = 'REPRODUCIBLE'
        """).fetchone()[0]

        failed = connection.execute("""
            SELECT COUNT(*)
            FROM predictions
            WHERE reproducibility_status = 'FAILED'
        """).fetchone()[0]

    finally:
        connection.close()

    percentage = (reproducible / total * 100) if total else 0
    result = "PASS" if total > 0 and percentage == 100 else "FAILED"

    return jsonify({
        "baseline_target": "100%",
        "experiment_result": result,
        "failed_predictions": failed,
        "measured_reproducibility_percentage": percentage,
        "reproducible_predictions": reproducible,
        "total_predictions": total
    })


# ---------------------------------------------------------
# FAILURE TESTS
# ---------------------------------------------------------

@app.route("/failure-tests")
def failure_tests():
    connection = get_connection()

    try:
        tests = [
            ("Missing Dataset Version", "dataset_versions",
             "dataset_version", "missing_dataset_v99"),
            ("Missing Code Version", "code_versions",
             "code_version", "missing_code_v99"),
            ("Missing Model Version", "model_artifacts",
             "model_version", "missing_model_v99")
        ]

        results = []

        for label, table, column, version in tests:
            row = connection.execute(
                f"SELECT 1 FROM {table} WHERE {column} = ?",
                (version,)
            ).fetchone()

            results.append({
                "test": label,
                "version": version,
                "result": (
                    "FAILED AS EXPECTED"
                    if not row
                    else "UNEXPECTED PASS"
                )
            })

        return jsonify(results)

    finally:
        connection.close()


# ---------------------------------------------------------
# AUDIT SUMMARY
# ---------------------------------------------------------

@app.route("/audit-summary")
def audit_summary():
    connection = get_connection()

    try:
        counts = {}

        for key, table in [
            ("dataset_versions", "dataset_versions"),
            ("model_artifacts", "model_artifacts"),
            ("approvals", "approvals"),
            ("deployments", "deployments"),
            ("historical_predictions", "predictions")
        ]:
            counts[key] = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

        counts["reproducible_predictions"] = connection.execute("""
            SELECT COUNT(*)
            FROM predictions
            WHERE reproducibility_status = 'REPRODUCIBLE'
        """).fetchone()[0]

        return jsonify({
            "project": "Model Reproducibility Registry",
            "status": "Registry implementation completed",
            **counts,
            "roles": ["ML Engineer", "Auditor"]
        })

    finally:
        connection.close()


# ---------------------------------------------------------
# DYNAMIC DASHBOARD
# ---------------------------------------------------------

@app.route("/dashboard")
def dashboard():
    connection = get_connection()

    try:
        dataset_versions = connection.execute("""
            SELECT COUNT(*) FROM dataset_versions
        """).fetchone()[0]

        model_artifacts = connection.execute("""
            SELECT COUNT(*) FROM model_artifacts
        """).fetchone()[0]

        approvals = connection.execute("""
            SELECT COUNT(*) FROM approvals
        """).fetchone()[0]

        deployments = connection.execute("""
            SELECT COUNT(*) FROM deployments
        """).fetchone()[0]

        historical_predictions = connection.execute("""
            SELECT COUNT(*) FROM predictions
        """).fetchone()[0]

        reproducible_predictions = connection.execute("""
            SELECT COUNT(*)
            FROM predictions
            WHERE reproducibility_status = 'REPRODUCIBLE'
        """).fetchone()[0]

    finally:
        connection.close()

    return render_template(
        "dashboard.html",
        dataset_versions=dataset_versions,
        model_artifacts=model_artifacts,
        approvals=approvals,
        deployments=deployments,
        historical_predictions=historical_predictions,
        reproducible_predictions=reproducible_predictions
    )


# ---------------------------------------------------------
# APPROVAL RECORDS PAGE
# ---------------------------------------------------------

@app.route("/approvals-page")
def approvals_page():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM approvals
            ORDER BY id
        """).fetchall()

        approvals = [dict(row) for row in rows]

    finally:
        connection.close()

    return render_template("approvals.html", approvals=approvals)


# ---------------------------------------------------------
# DATASET VERSIONS PAGE
# ---------------------------------------------------------

@app.route("/datasets-page")
def datasets_page():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM dataset_versions
            ORDER BY id
        """).fetchall()

        datasets = [dict(row) for row in rows]

    finally:
        connection.close()

    return render_template("datasets.html", datasets=datasets)


# ---------------------------------------------------------
# MODEL ARTIFACTS PAGE
# ---------------------------------------------------------

@app.route("/models-page")
def models_page():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM model_artifacts
            ORDER BY id
        """).fetchall()

        models = [dict(row) for row in rows]

    finally:
        connection.close()

    return render_template("models.html", models=models)


# ---------------------------------------------------------
# DEPLOYMENTS PAGE
# ---------------------------------------------------------

@app.route("/deployments-page")
def deployments_page():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM deployments
            ORDER BY id
        """).fetchall()

        deployments = [dict(row) for row in rows]

    finally:
        connection.close()

    return render_template(
        "deployments.html",
        deployments=deployments
    )


# ---------------------------------------------------------
# HISTORICAL PREDICTIONS PAGE
# ---------------------------------------------------------

@app.route("/predictions-page")
def predictions_page():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM predictions
            ORDER BY id
        """).fetchall()

        predictions = [dict(row) for row in rows]

    finally:
        connection.close()

    return render_template(
        "predictions.html",
        predictions=predictions
    )


# ---------------------------------------------------------
# REPRODUCIBLE PREDICTIONS PAGE
# ---------------------------------------------------------

@app.route("/reproducible-page")
def reproducible_page():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM predictions
            WHERE reproducibility_status = 'REPRODUCIBLE'
            ORDER BY id
        """).fetchall()

        predictions = [dict(row) for row in rows]

    finally:
        connection.close()

    return render_template(
        "reproducible.html",
        predictions=predictions
    )


# ---------------------------------------------------------
# REGISTER DATASET SCHEMA
# ---------------------------------------------------------

@app.route("/register-schema/<dataset_version>")
def register_schema(dataset_version):
    connection = get_connection()

    try:
        dataset = connection.execute("""
            SELECT file_path
            FROM dataset_versions
            WHERE dataset_version = ?
        """, (dataset_version,)).fetchone()

        if not dataset:
            return jsonify({
                "status": "FAILED",
                "message": "Dataset version not found. Register it first."
            }), 404

        existing_count = connection.execute("""
            SELECT COUNT(*)
            FROM dataset_schemas
            WHERE dataset_version = ?
        """, (dataset_version,)).fetchone()[0]

        if existing_count:
            return jsonify({
                "status": "EXISTS",
                "message": "Schema is already registered.",
                "dataset_version": dataset_version,
                "registered_columns": existing_count
            }), 409

        path = resolve_dataset_file(dataset["file_path"])
        schema = read_csv_schema(path)

        connection.executemany("""
            INSERT INTO dataset_schemas
            (dataset_version, column_name, data_type, nullable)
            VALUES (?, ?, ?, ?)
        """, [
            (
                dataset_version,
                column_name,
                details["data_type"],
                details["nullable"]
            )
            for column_name, details in schema.items()
        ])

        connection.commit()

        return jsonify({
            "status": "SUCCESS",
            "message": "Dataset schema registered successfully.",
            "dataset_version": dataset_version,
            "registered_columns": schema
        }), 201

    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        connection.rollback()
        return jsonify({
            "status": "FAILED",
            "message": str(error)
        }), 400

    except Exception as error:
        connection.rollback()
        app.logger.exception("Schema registration error")
        return jsonify({
            "status": "FAILED",
            "message": str(error)
        }), 500

    finally:
        connection.close()


# ---------------------------------------------------------
# CHECK DATASET SCHEMA DRIFT
# ---------------------------------------------------------

@app.route("/check-schema-drift/<dataset_version>")
def check_schema_drift(dataset_version):
    connection = get_connection()

    try:
        dataset = connection.execute("""
            SELECT file_path
            FROM dataset_versions
            WHERE dataset_version = ?
        """, (dataset_version,)).fetchone()

        if not dataset:
            return jsonify({
                "status": "FAILED",
                "message": "Dataset version not found."
            }), 404

        expected_rows = connection.execute("""
            SELECT column_name, data_type, nullable
            FROM dataset_schemas
            WHERE dataset_version = ?
        """, (dataset_version,)).fetchall()

        if not expected_rows:
            return jsonify({
                "status": "FAILED",
                "message": (
                    "Schema not registered. Register the schema first."
                )
            }), 400

        expected = {
            row["column_name"]: {
                "data_type": row["data_type"],
                "nullable": row["nullable"]
            }
            for row in expected_rows
        }

        path = resolve_dataset_file(dataset["file_path"])
        actual = read_csv_schema(path)

        expected_columns = set(expected)
        actual_columns = set(actual)

        added_columns = sorted(actual_columns - expected_columns)
        missing_columns = sorted(expected_columns - actual_columns)

        type_changes = []
        nullability_changes = []

        for column in sorted(expected_columns & actual_columns):
            old_type = expected[column]["data_type"]
            new_type = actual[column]["data_type"]

            if old_type != new_type:
                type_changes.append({
                    "column": column,
                    "registered_type": old_type,
                    "current_type": new_type
                })

            if (
                expected[column]["nullable"] == 0
                and actual[column]["nullable"] == 1
            ):
                nullability_changes.append({
                    "column": column,
                    "issue": "New empty values detected"
                })

        drift_detected = bool(
            added_columns
            or missing_columns
            or type_changes
            or nullability_changes
        )

        return jsonify({
            "dataset_version": dataset_version,
            "status": (
                "DRIFT DETECTED"
                if drift_detected
                else "NO DRIFT"
            ),
            "added_columns": added_columns,
            "missing_columns": missing_columns,
            "type_changes": type_changes,
            "nullability_changes": nullability_changes
        })

    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        return jsonify({
            "status": "FAILED",
            "message": str(error)
        }), 400

    except Exception as error:
        app.logger.exception("Schema drift check error")
        return jsonify({
            "status": "FAILED",
            "message": str(error)
        }), 500

    finally:
        connection.close()


# ---------------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)