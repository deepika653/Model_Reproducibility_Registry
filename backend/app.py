from flask import Flask, jsonify, render_template
from pathlib import Path
from database import init_database, get_connection


# ---------------------------------------------------------
# APPLICATION SETUP
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates")
)

# Initialize Database
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
# VIEW DATASETS
# ---------------------------------------------------------

@app.route("/datasets")
def get_datasets():

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM dataset_versions
        ORDER BY id
    """).fetchall()

    connection.close()

    return jsonify([dict(row) for row in rows])


# ---------------------------------------------------------
# REGISTER FEATURES
# ---------------------------------------------------------

@app.route("/register-features")
def register_features():

    connection = get_connection()

    features = [

        (
            "feature_v1",
            "age",
            "Patient age in years",
            "integer"
        ),

        (
            "feature_v2",
            "gender",
            "Patient gender category",
            "categorical"
        ),

        (
            "feature_v3",
            "blood_pressure",
            "Patient blood pressure measurement",
            "integer"
        ),

        (
            "feature_v4",
            "glucose_level",
            "Patient glucose level measurement",
            "integer"
        ),

        (
            "feature_v5",
            "heart_rate",
            "Patient heart rate measurement",
            "integer"
        ),

        (
            "feature_v6",
            "symptom_score",
            "Patient symptom severity score from 0 to 10",
            "integer"
        )

    ]

    connection.executemany("""
        INSERT OR IGNORE INTO feature_definitions
        (feature_version, feature_name, definition, data_type)
        VALUES (?, ?, ?, ?)
    """, features)

    connection.commit()
    connection.close()

    return "Features registered successfully!"


# ---------------------------------------------------------
# VIEW FEATURES
# ---------------------------------------------------------

@app.route("/features")
def get_features():

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM feature_definitions
        ORDER BY id
    """).fetchall()

    connection.close()

    return jsonify([dict(row) for row in rows])


# ---------------------------------------------------------
# REGISTER CODE VERSION
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
        "Model_Reproducibility_Registry"
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
        SELECT *
        FROM code_versions
        ORDER BY id
    """).fetchall()

    connection.close()

    return jsonify([dict(row) for row in rows])


# ---------------------------------------------------------
# REGISTER MODEL
# ---------------------------------------------------------

@app.route("/register-model")
def register_model():

    connection = get_connection()

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
    connection.close()

    return "model_v1 registered successfully!"


# ---------------------------------------------------------
# VIEW MODELS
# ---------------------------------------------------------

@app.route("/models")
def get_models():

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM model_artifacts
        ORDER BY id
    """).fetchall()

    connection.close()

    return jsonify([dict(row) for row in rows])


# ---------------------------------------------------------
# REGISTER APPROVAL
# ---------------------------------------------------------

@app.route("/register-approval")
def register_approval():

    connection = get_connection()

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
    connection.close()

    return "Model approval registered successfully!"


# ---------------------------------------------------------
# VIEW APPROVALS
# ---------------------------------------------------------

@app.route("/approvals")
def get_approvals():

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM approvals
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
    connection.close()

    return "deployment_v1 registered successfully!"


# ---------------------------------------------------------
# VIEW DEPLOYMENTS
# ---------------------------------------------------------

@app.route("/deployments")
def get_deployments():

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM deployments
        ORDER BY id
    """).fetchall()

    connection.close()

    return jsonify([dict(row) for row in rows])


# ---------------------------------------------------------
# VIEW PREDICTIONS
# ---------------------------------------------------------

@app.route("/predictions")
def get_predictions():

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM predictions
        ORDER BY id
    """).fetchall()

    connection.close()

    return jsonify([dict(row) for row in rows])


# ---------------------------------------------------------
# REPRODUCIBILITY VALIDATION
# ---------------------------------------------------------

@app.route("/validate-reproducibility")
def validate_reproducibility():

    connection = get_connection()

    predictions = connection.execute("""
        SELECT *
        FROM predictions
        ORDER BY id
    """).fetchall()

    results = []

    for prediction in predictions:

        failure_reasons = []

        dataset = connection.execute("""
            SELECT *
            FROM dataset_versions
            WHERE dataset_version = ?
        """, (
            prediction["dataset_version"],
        )).fetchone()

        if not dataset:
            failure_reasons.append(
                "Dataset version not found"
            )

        feature = connection.execute("""
            SELECT *
            FROM feature_definitions
            WHERE feature_version = ?
        """, (
            prediction["feature_version"],
        )).fetchone()

        if not feature:
            failure_reasons.append(
                "Feature version not found"
            )

        code = connection.execute("""
            SELECT *
            FROM code_versions
            WHERE code_version = ?
        """, (
            prediction["code_version"],
        )).fetchone()

        if not code:
            failure_reasons.append(
                "Code version not found"
            )

        model = connection.execute("""
            SELECT *
            FROM model_artifacts
            WHERE model_version = ?
        """, (
            prediction["model_version"],
        )).fetchone()

        if not model:
            failure_reasons.append(
                "Model version not found"
            )

        if len(failure_reasons) == 0:

            status = "REPRODUCIBLE"

            connection.execute("""
                UPDATE predictions
                SET reproducibility_status = ?,
                failure_reason = ?
                WHERE id = ?
            """, (
                status,
                None,
                prediction["id"]
            ))

        else:

            status = "FAILED"

            failure_reason = "; ".join(
                failure_reasons
            )

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

            "prediction_id":
            prediction["id"],

            "patient_id":
            prediction["patient_id"],

            "status":
            status,

            "failure_reason":
            None if len(failure_reasons) == 0
            else "; ".join(failure_reasons)

        })

    connection.commit()
    connection.close()

    return jsonify(results)


# ---------------------------------------------------------
# REPRODUCIBILITY EXPERIMENT
# ---------------------------------------------------------

@app.route("/reproducibility-experiment")
def reproducibility_experiment():

    connection = get_connection()

    total_predictions = connection.execute("""
        SELECT COUNT(*)
        FROM predictions
    """).fetchone()[0]

    reproducible_predictions = connection.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE reproducibility_status = 'REPRODUCIBLE'
    """).fetchone()[0]

    failed_predictions = connection.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE reproducibility_status = 'FAILED'
    """).fetchone()[0]

    connection.close()

    if total_predictions > 0:

        percentage = (
            reproducible_predictions /
            total_predictions
        ) * 100

    else:

        percentage = 0

    result = "PASS"

    if percentage < 100:
        result = "FAILED"

    return jsonify({

        "baseline_target":
        "100%",

        "experiment_result":
        result,

        "failed_predictions":
        failed_predictions,

        "measured_reproducibility_percentage":
        percentage,

        "reproducible_predictions":
        reproducible_predictions,

        "total_predictions":
        total_predictions

    })
# ---------------------------------------------------------
# FAILURE TESTS
# ---------------------------------------------------------

@app.route("/failure-tests")
def failure_tests():

    connection = get_connection()

    tests = []

    # Test 1: Missing Dataset Version
    dataset = connection.execute("""
        SELECT *
        FROM dataset_versions
        WHERE dataset_version = ?
    """, (
        "missing_dataset_v99",
    )).fetchone()

    tests.append({
        "test": "Missing Dataset Version",
        "version": "missing_dataset_v99",
        "result": "FAILED AS EXPECTED"
        if not dataset else "UNEXPECTED PASS"
    })

    # Test 2: Missing Code Version
    code = connection.execute("""
        SELECT *
        FROM code_versions
        WHERE code_version = ?
    """, (
        "missing_code_v99",
    )).fetchone()

    tests.append({
        "test": "Missing Code Version",
        "version": "missing_code_v99",
        "result": "FAILED AS EXPECTED"
        if not code else "UNEXPECTED PASS"
    })

    # Test 3: Missing Model Version
    model = connection.execute("""
        SELECT *
        FROM model_artifacts
        WHERE model_version = ?
    """, (
        "missing_model_v99",
    )).fetchone()

    tests.append({
        "test": "Missing Model Version",
        "version": "missing_model_v99",
        "result": "FAILED AS EXPECTED"
        if not model else "UNEXPECTED PASS"
    })

    connection.close()

    return jsonify(tests)

# ---------------------------------------------------------
# AUDIT SUMMARY
# ---------------------------------------------------------

@app.route("/audit-summary")
def audit_summary():

    connection = get_connection()

    dataset_versions = connection.execute("""
        SELECT COUNT(*)
        FROM dataset_versions
    """).fetchone()[0]

    model_artifacts = connection.execute("""
        SELECT COUNT(*)
        FROM model_artifacts
    """).fetchone()[0]

    approvals = connection.execute("""
        SELECT COUNT(*)
        FROM approvals
    """).fetchone()[0]

    deployments = connection.execute("""
        SELECT COUNT(*)
        FROM deployments
    """).fetchone()[0]

    historical_predictions = connection.execute("""
        SELECT COUNT(*)
        FROM predictions
    """).fetchone()[0]

    reproducible_predictions = connection.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE reproducibility_status =
        'REPRODUCIBLE'
    """).fetchone()[0]

    connection.close()

    return jsonify({

        "project":
        "Model Reproducibility Registry",

        "status":
        "Registry implementation completed",

        "dataset_versions":
        dataset_versions,

        "model_artifacts":
        model_artifacts,

        "approvals":
        approvals,

        "deployments":
        deployments,

        "historical_predictions":
        historical_predictions,

        "reproducible_predictions":
        reproducible_predictions,

        "roles": [
            "ML Engineer",
            "Auditor"
        ]

    })


# ---------------------------------------------------------
# DYNAMIC DASHBOARD
# ---------------------------------------------------------

@app.route("/dashboard")
def dashboard():

    connection = get_connection()

    dataset_versions = connection.execute("""
        SELECT COUNT(*)
        FROM dataset_versions
    """).fetchone()[0]

    model_artifacts = connection.execute("""
        SELECT COUNT(*)
        FROM model_artifacts
    """).fetchone()[0]

    approvals = connection.execute("""
        SELECT COUNT(*)
        FROM approvals
    """).fetchone()[0]

    deployments = connection.execute("""
        SELECT COUNT(*)
        FROM deployments
    """).fetchone()[0]

    historical_predictions = connection.execute("""
        SELECT COUNT(*)
        FROM predictions
    """).fetchone()[0]

    reproducible_predictions = connection.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE reproducibility_status =
        'REPRODUCIBLE'
    """).fetchone()[0]

    connection.close()

    return render_template(

        "dashboard.html",

        dataset_versions=
        dataset_versions,

        model_artifacts=
        model_artifacts,

        approvals=
        approvals,

        deployments=
        deployments,

        historical_predictions=
        historical_predictions,

        reproducible_predictions=
        reproducible_predictions

    )
# ---------------------------------------------------------
# APPROVAL RECORDS PAGE
# ---------------------------------------------------------

@app.route("/approvals-page")
def approvals_page():

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM approvals
        ORDER BY id
    """).fetchall()

    connection.close()

    approvals = [dict(row) for row in rows]

    return render_template(
        "approvals.html",
        approvals=approvals
    )
# ---------------------------------------------------------
# DATASET VERSIONS PAGE
# ---------------------------------------------------------

@app.route("/datasets-page")
def datasets_page():

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM dataset_versions
        ORDER BY id
    """).fetchall()

    connection.close()

    datasets = [dict(row) for row in rows]

    return render_template(
        "datasets.html",
        datasets=datasets
    )
# ---------------------------------------------------------
# MODEL ARTIFACTS PAGE
# ---------------------------------------------------------

@app.route("/models-page")
def models_page():

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM model_artifacts
        ORDER BY id
    """).fetchall()

    connection.close()

    models = [dict(row) for row in rows]

    return render_template(
        "models.html",
        models=models
    )
# ---------------------------------------------------------
# DEPLOYMENTS PAGE
# ---------------------------------------------------------

@app.route("/deployments-page")
def deployments_page():

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM deployments
        ORDER BY id
    """).fetchall()

    connection.close()

    deployments = [dict(row) for row in rows]

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

    rows = connection.execute("""
        SELECT *
        FROM predictions
        ORDER BY id
    """).fetchall()

    connection.close()

    predictions = [dict(row) for row in rows]

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

    rows = connection.execute("""
        SELECT *
        FROM predictions
        WHERE reproducibility_status = 'REPRODUCIBLE'
        ORDER BY id
    """).fetchall()

    connection.close()

    predictions = [dict(row) for row in rows]

    return render_template(
        "reproducible.html",
        predictions=predictions
    )

# ---------------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )