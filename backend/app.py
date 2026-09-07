from flask import Flask, jsonify
from database import init_database, get_connection

app = Flask(__name__)

init_database()


@app.route("/")
def home():
    return "Model Reproducibility Registry is running!"
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
            "feature_v1",
            "gender",
            "Patient gender category",
            "categorical"
        ),
        (
            "feature_v1",
            "blood_pressure",
            "Patient blood pressure measurement",
            "integer"
        ),
        (
            "feature_v1",
            "glucose_level",
            "Patient glucose level measurement",
            "integer"
        ),
        (
            "feature_v1",
            "heart_rate",
            "Patient heart rate measurement",
            "integer"
        ),
        (
            "feature_v1",
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

    return "feature_v1 registered successfully!"
@app.route("/datasets")
def get_datasets():
    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM dataset_versions
        ORDER BY id
    """).fetchall()

    connection.close()

    datasets = [dict(row) for row in rows]

    return jsonify(datasets)


if __name__ == "__main__":
    app.run(debug=True)