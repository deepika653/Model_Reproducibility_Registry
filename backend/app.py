
from flask import Flask, jsonify, render_template
from pathlib import Path
from database import init_database, get_connection

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates")
)

# Initialize database
init_database()


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
    connection.close()

    return "dataset_v1 registered successfully!"


# ---------------------------------------------------------
# REGISTER FEATURES
# ---------------------------------------------------------
@app.route("/register-features")
def register_features():
    connection = get_connection()

    features = [
        ("feature_v1", "age", "Patient age in years", "integer"),
        ("feature_v1", "gender", "Patient gender category", "categorical"),
        ("feature_v1", "blood_pressure", "Patient blood pressure measurement", "integer"),
        ("feature_v1", "glucose_level", "Patient glucose level measurement", "integer"),
        ("feature_v1", "heart_rate", "Patient heart rate measurement", "integer"),
        ("feature_v1", "symptom_score",
         "Patient symptom severity score from 0 to 10", "integer")
    ]

    connection.executemany("""
        INSERT OR IGNORE INTO feature_definitions
        (feature_version, feature_name, definition, data_type)
        VALUES (?, ?, ?, ?)
    """, features)

    connection.commit()
    connection.close()

    return "feature_v1 registered successfully!"


# ---------------------------------------------------------
# VIEW FEATURES
# ---------------------------------------------------------
@app.route("/features")
def get_features():
    connection = get_connection()

    rows = connection.execute("""
        SELECT * FROM feature_definitions
        ORDER BY id
    """).fetchall()

    connection.close()
    return jsonify([dict(row) for row in rows])


# ---------------------------------------------------------
# REGISTER CODE VERSION / GIT COMMIT
# ROLE: ML ENGINEER
# ---------------------------------------------------------
@app.route("/register-code")
def register_code():
    connection = get_connection()

    connection.execute("""
        INSERT OR IGNORE INTO code_versions
        (code_version, commit_hash, repository)
        VALUES (?, ?, ?)
    """, (
        "code_v1",
        "66e5b85",
        "Model_Registry"
    ))

    connection.commit()
    connection.close()

    return "code_v1 registered successfully!"


# ---------------------------------------------------------
# VIEW CODE VERSIONS
# ---------------------------------------------------------
@app.route("/code-versions")
def get_code_versions():
    connection = get_connection()

    rows = connection.execute("""
        SELECT * FROM code_versions
        ORDER BY id
    """).fetchall()

    connection.close()
    return jsonify([dict(row) for row in rows])


# ---------------------------------------------------------
# REGISTER MODEL ARTIFACT
# ROLE: ML ENGINEER
# ---------------------------------------------------------
@app.route("/register-model")
def register_model():
    connection = get_connection()

    connection.execute("""
        INSERT OR IGNORE INTO model_artifacts
        (model_version, model_name, artifact_path, algorithm, parameters)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "model_v1",
        "Hospital Risk Prediction Model",
        "models/model_v1.pkl",
        "DecisionTreeClassifier",
        "max_depth=5, random_state=42, accuracy=98.8%"
    ))

    connection.commit()
    connection.close()

    return "model_v1 registered successfully!"


# ---------------------------------------------------------
# VIEW MODEL ARTIFACTS
# ---------------------------------------------------------
@app.route("/models")
def get_models():
    connection = get_connection()

    rows = connection.execute("""
        SELECT * FROM model_artifacts
        ORDER BY id
    """).fetchall()

    connection.close()
    return jsonify([dict(row) for row in rows])


# ---------------------------------------------------------
# REGISTER MODEL APPROVAL
# ROLE: AUDITOR
# ---------------------------------------------------------
@app.route("/register-approval")
def register_approval():
    connection = get_connection()

    connection.execute("""
        INSERT INTO approvals
        (model_version, approved_by, role, approval_status, comments)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "model_v1",
        "Hospital Auditor",
        "Auditor",
        "APPROVED",
        "Model reviewed for reproducibility and audit tracking"
    ))

    connection.commit()
    connection.close()

    return "model_v1 approved successfully by Auditor!"


# ---------------------------------------------------------
# VIEW APPROVALS
# ---------------------------------------------------------
@app.route("/approvals")
def get_approvals():
    connection = get_connection()

    rows = connection.execute("""
        SELECT * FROM approvals
        ORDER BY id
    """).fetchall()

    connection.close()
    return jsonify([dict(row) for row in rows])


# ---------------------------------------------------------
# REGISTER DEPLOYMENT
# ---------------------------------------------------------
@app.route("/register-deployment")
def register_deployment():
    connection = get_connection()

    connection.execute("""
        INSERT OR IGNORE INTO deployments
        (deployment_version, model_version, environment,
         deployed_by, deployment_status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "deployment_v1",
        "model_v1",
        "Testing",
        "ML Engineer",
        "DEPLOYED"
    ))

    connection.commit()
    connection.close()

    return "deployment_v1 registered successfully!"


# ---------------------------------------------------------
# VIEW DEPLOYMENTS
# ---------------------------------------------------------
@app.route("/deployments")
def get_deployments():
    connection = get_connection()

    rows = connection.execute("""
        SELECT * FROM deployments
        ORDER BY id
    """).fetchall()

    connection.close()
    return jsonify([dict(row) for row in rows])


# ---------------------------------------------------------
# CREATE HISTORICAL PREDICTIONS
# ---------------------------------------------------------
@app.route("/create-predictions")
def create_predictions():
    connection = get_connection()

    predictions = [
        (
            "P001", "Medium",
            "dataset_v1", "feature_v1", "code_v1",
            "model_v1", "deployment_v1",
            "max_depth=5, random_state=42",
            "UNKNOWN", None
        ),
        (
            "P002", "High",
            "dataset_v1", "feature_v1", "code_v1",
            "model_v1", "deployment_v1",
            "max_depth=5, random_state=42",
            "UNKNOWN", None
        ),
        (
            "P003", "Low",
            "dataset_v1", "feature_v1", "code_v1",
            "model_v1", "deployment_v1",
            "max_depth=5, random_state=42",
            "UNKNOWN", None
        ),
        (
            "P004", "High",
            "dataset_v1", "feature_v1", "code_v1",
            "model_v1", "deployment_v1",
            "max_depth=5, random_state=42",
            "UNKNOWN", None
        ),
        (
            "P005", "High",
            "dataset_v1", "feature_v1", "code_v1",
            "model_v1", "deployment_v1",
            "max_depth=5, random_state=42",
            "UNKNOWN", None
        )
    ]

    connection.executemany("""
        INSERT INTO predictions (
            patient_id, prediction,
            dataset_version, feature_version, code_version,
            model_version, deployment_version,
            parameters, reproducibility_status, failure_reason
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, predictions)

    connection.commit()
    connection.close()

    return "5 historical predictions created successfully!"


# ---------------------------------------------------------
# VIEW HISTORICAL PREDICTIONS
# ---------------------------------------------------------
@app.route("/predictions")
def get_predictions():
    connection = get_connection()

    rows = connection.execute("""
        SELECT * FROM predictions
        ORDER BY id
    """).fetchall()

    connection.close()

    return jsonify([dict(row) for row in rows])


# ---------------------------------------------------------
# VIEW DATASETS
# ---------------------------------------------------------
@app.route("/datasets")
def get_datasets():
    connection = get_connection()

    rows = connection.execute("""
        SELECT * FROM dataset_versions
        ORDER BY id
    """).fetchall()

    connection.close()

    return jsonify([dict(row) for row in rows])

# ---------------------------------------------------------
# VALIDATE REPRODUCIBILITY
# ---------------------------------------------------------
@app.route("/validate-predictions")
def validate_predictions():

    connection = get_connection()

    predictions = connection.execute("""
        SELECT * FROM predictions
        ORDER BY id
    """).fetchall()

    results = []

    for prediction in predictions:

        failure_reasons = []

        # Check Dataset
        dataset = connection.execute("""
            SELECT * FROM dataset_versions
            WHERE dataset_version = ?
        """, (prediction["dataset_version"],)).fetchone()

        if not dataset:
            failure_reasons.append("Dataset version not found")

        # Check Features
        features = connection.execute("""
            SELECT * FROM feature_definitions
            WHERE feature_version = ?
        """, (prediction["feature_version"],)).fetchone()

        if not features:
            failure_reasons.append("Feature version not found")

        # Check Code
        code = connection.execute("""
            SELECT * FROM code_versions
            WHERE code_version = ?
        """, (prediction["code_version"],)).fetchone()

        if not code:
            failure_reasons.append("Code version not found")

        # Check Model
        model = connection.execute("""
            SELECT * FROM model_artifacts
            WHERE model_version = ?
        """, (prediction["model_version"],)).fetchone()

        if not model:
            failure_reasons.append("Model version not found")
        else:
            model_path = Path(__file__).resolve().parent.parent / model["artifact_path"]

            if not model_path.exists():
                failure_reasons.append("Model artifact file not found")

        # Check Deployment
        deployment = connection.execute("""
            SELECT * FROM deployments
            WHERE deployment_version = ?
        """, (prediction["deployment_version"],)).fetchone()

        if not deployment:
            failure_reasons.append("Deployment version not found")

        # Check Approval
        approval = connection.execute("""
            SELECT * FROM approvals
            WHERE model_version = ?
            AND approval_status = 'APPROVED'
        """, (prediction["model_version"],)).fetchone()

        if not approval:
            failure_reasons.append("Approved model record not found")

        # Update Reproducibility Status
        if len(failure_reasons) == 0:
            status = "REPRODUCIBLE"
            reason = None
        else:
            status = "FAILED"
            reason = "; ".join(failure_reasons)

        connection.execute("""
            UPDATE predictions
            SET reproducibility_status = ?,
                failure_reason = ?
            WHERE id = ?
        """, (
            status,
            reason,
            prediction["id"]
        ))

        results.append({
            "prediction_id": prediction["id"],
            "patient_id": prediction["patient_id"],
            "status": status,
            "failure_reason": reason
        })

    connection.commit()
    connection.close()

    return jsonify(results)


# ---------------------------------------------------------
# RUN FAILURE TESTS
# ---------------------------------------------------------
@app.route("/failure-tests")
def failure_tests():

    connection = get_connection()

    results = []

    # Failure Test 1 - Missing Dataset
    dataset = connection.execute("""
        SELECT * FROM dataset_versions
        WHERE dataset_version = ?
    """, ("missing_dataset_v99",)).fetchone()

    results.append({
        "test": "Missing Dataset Version",
        "version": "missing_dataset_v99",
        "result": "FAILED AS EXPECTED" if not dataset else "UNEXPECTED PASS"
    })

    # Failure Test 2 - Missing Code
    code = connection.execute("""
        SELECT * FROM code_versions
        WHERE code_version = ?
    """, ("missing_code_v99",)).fetchone()

    results.append({
        "test": "Missing Code Version",
        "version": "missing_code_v99",
        "result": "FAILED AS EXPECTED" if not code else "UNEXPECTED PASS"
    })

    # Failure Test 3 - Missing Model
    model = connection.execute("""
        SELECT * FROM model_artifacts
        WHERE model_version = ?
    """, ("missing_model_v99",)).fetchone()

    results.append({
        "test": "Missing Model Version",
        "version": "missing_model_v99",
        "result": "FAILED AS EXPECTED" if not model else "UNEXPECTED PASS"
    })

    connection.close()

    return jsonify(results)


# ---------------------------------------------------------
# REPRODUCIBILITY EXPERIMENT REPORT
# ---------------------------------------------------------
@app.route("/reproducibility-report")
def reproducibility_report():

    connection = get_connection()

    total = connection.execute("""
        SELECT COUNT(*) AS count
        FROM predictions
    """).fetchone()["count"]

    reproducible = connection.execute("""
        SELECT COUNT(*) AS count
        FROM predictions
        WHERE reproducibility_status = 'REPRODUCIBLE'
    """).fetchone()["count"]

    failed = connection.execute("""
        SELECT COUNT(*) AS count
        FROM predictions
        WHERE reproducibility_status = 'FAILED'
    """).fetchone()["count"]

    if total > 0:
        reproducibility_percentage = round(
            (reproducible / total) * 100,
            2
        )
    else:
        reproducibility_percentage = 0

    connection.close()

    return jsonify({
        "total_predictions": total,
        "reproducible_predictions": reproducible,
        "failed_predictions": failed,
        "measured_reproducibility_percentage": reproducibility_percentage,
        "baseline_target": "100%",
        "experiment_result": "PASS"
        if reproducibility_percentage == 100
        else "NEEDS REVIEW"
    })


# ---------------------------------------------------------
# REGISTER REGISTRY RULES
# ---------------------------------------------------------
@app.route("/register-rules")
def register_rules():

    connection = get_connection()

    rules = [
        (
            "dataset_required",
            "Every prediction must have a registered dataset version",
            "True"
        ),
        (
            "feature_required",
            "Every prediction must have a registered feature version",
            "True"
        ),
        (
            "code_required",
            "Every prediction must have a registered code version",
            "True"
        ),
        (
            "model_required",
            "Every prediction must have a registered model artifact",
            "True"
        ),
        (
            "approval_required",
            "Model must be approved by an Auditor",
            "True"
        )
    ]

    connection.executemany("""
        INSERT OR IGNORE INTO registry_rules
        (rule_name, rule_description, rule_value)
        VALUES (?, ?, ?)
    """, rules)

    connection.commit()
    connection.close()

    return "Registry rules registered successfully!"


# ---------------------------------------------------------
# VIEW REGISTRY RULES
# ---------------------------------------------------------
@app.route("/rules")
def get_rules():

    connection = get_connection()

    rows = connection.execute("""
        SELECT * FROM registry_rules
        ORDER BY id
    """).fetchall()

    connection.close()

    return jsonify([dict(row) for row in rows])


# ---------------------------------------------------------
# FINAL AUDIT SUMMARY
# ---------------------------------------------------------
@app.route("/audit-summary")
def audit_summary():

    connection = get_connection()

    datasets = connection.execute(
        "SELECT COUNT(*) AS count FROM dataset_versions"
    ).fetchone()["count"]

    models = connection.execute(
        "SELECT COUNT(*) AS count FROM model_artifacts"
    ).fetchone()["count"]

    approvals = connection.execute(
        "SELECT COUNT(*) AS count FROM approvals"
    ).fetchone()["count"]

    deployments = connection.execute(
        "SELECT COUNT(*) AS count FROM deployments"
    ).fetchone()["count"]

    predictions = connection.execute(
        "SELECT COUNT(*) AS count FROM predictions"
    ).fetchone()["count"]

    reproducible = connection.execute("""
        SELECT COUNT(*) AS count
        FROM predictions
        WHERE reproducibility_status = 'REPRODUCIBLE'
    """).fetchone()["count"]

    connection.close()

    return jsonify({
        "project": "Model Reproducibility Registry",
        "dataset_versions": datasets,
        "model_artifacts": models,
        "approvals": approvals,
        "deployments": deployments,
        "historical_predictions": predictions,
        "reproducible_predictions": reproducible,
        "roles": [
            "ML Engineer",
            "Auditor"
        ],
        "status": "Registry implementation completed"
    })
# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
# ---------------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)