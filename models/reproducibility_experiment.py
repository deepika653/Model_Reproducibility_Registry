
import hashlib
import json
import joblib
import pandas as pd

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "dataset_v1.csv"
REPORT_PATH = BASE_DIR / "models" / "reproducibility_report.json"


# ---------------------------------------------------------
# EXPERIMENT CONFIGURATION
# ---------------------------------------------------------

FEATURE_COLUMNS = [
    "age",
    "gender",
    "blood_pressure",
    "glucose_level",
    "heart_rate",
    "symptom_score"
]

TARGET_COLUMN = "risk_level"

RANDOM_STATE = 42
TEST_SIZE = 0.2


# ---------------------------------------------------------
# HASH FUNCTION
# ---------------------------------------------------------

def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of a saved model file."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


# ---------------------------------------------------------
# LOAD AND PREPARE DATA
# ---------------------------------------------------------

def load_and_prepare_data():
    """Load dataset and prepare features and target."""

    if not DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully!")
    print("Dataset shape:", df.shape)

    missing_columns = [
        column
        for column in FEATURE_COLUMNS + [TARGET_COLUMN]
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()

    if X.isnull().any().any() or y.isnull().any():
        raise ValueError(
            "Dataset contains missing values in required columns."
        )

    gender_encoder = LabelEncoder()
    X["gender"] = gender_encoder.fit_transform(
        X["gender"].astype(str)
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        gender_encoder
    )


# ---------------------------------------------------------
# TRAIN AN INDEPENDENT MODEL
# ---------------------------------------------------------

def train_experiment_model(
    X_train,
    y_train,
    X_test,
    y_test,
    experiment_name
):
    """Train and evaluate a model without replacing model_v1."""

    model = DecisionTreeClassifier(
        max_depth=5,
        random_state=RANDOM_STATE
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    artifact_path = (
        BASE_DIR / "models" / f"{experiment_name}.pkl"
    )

    model_data = {
        "model": model,
        "feature_columns": FEATURE_COLUMNS,
        "accuracy": accuracy,
        "dataset_version": "dataset_v1",
        "feature_version": "feature_v1",
        "random_state": RANDOM_STATE,
        "test_size": TEST_SIZE
    }

    joblib.dump(model_data, artifact_path)

    artifact_hash = calculate_file_hash(artifact_path)

    print(f"\n{experiment_name}")
    print("Accuracy:", round(accuracy * 100, 2), "%")
    print("Artifact:", artifact_path)
    print("SHA-256:", artifact_hash)

    return {
        "experiment_name": experiment_name,
        "accuracy": accuracy,
        "predictions": predictions.tolist(),
        "artifact_path": str(artifact_path),
        "artifact_hash": artifact_hash
    }


# ---------------------------------------------------------
# RUN REPRODUCIBILITY EXPERIMENT
# ---------------------------------------------------------

def run_reproducibility_experiment():
    """Train two models and compare their results."""

    (
        X_train,
        X_test,
        y_train,
        y_test,
        gender_encoder
    ) = load_and_prepare_data()

    print("\nStarting independent training runs...")

    run_1 = train_experiment_model(
        X_train,
        y_train,
        X_test,
        y_test,
        "reproducibility_run_1"
    )

    run_2 = train_experiment_model(
        X_train,
        y_train,
        X_test,
        y_test,
        "reproducibility_run_2"
    )

    predictions_match = (
        run_1["predictions"] == run_2["predictions"]
    )

    accuracy_match = (
        run_1["accuracy"] == run_2["accuracy"]
    )

    artifact_hash_match = (
        run_1["artifact_hash"] == run_2["artifact_hash"]
    )

    reproducible = (
        predictions_match
        and accuracy_match
    )

    # -----------------------------------------------------
    # EXPERIMENT REPORT
    # -----------------------------------------------------

    report = {
        "experiment": "Fresh Model Retraining Reproducibility",
        "dataset": "dataset_v1",
        "feature_version": "feature_v1",
        "model_type": "DecisionTreeClassifier",
        "model_parameters": {
            "max_depth": 5,
            "random_state": RANDOM_STATE
        },
        "test_size": TEST_SIZE,
        "training_runs": 2,
        "run_1_accuracy": run_1["accuracy"],
        "run_2_accuracy": run_2["accuracy"],
        "predictions_match": predictions_match,
        "accuracy_match": accuracy_match,
        "artifact_hash_match": artifact_hash_match,
        "run_1_artifact_hash": run_1["artifact_hash"],
        "run_2_artifact_hash": run_2["artifact_hash"],
        "result": (
            "PASS"
            if reproducible
            else "FAIL"
        ),
        "interpretation": (
            "Both training runs produced matching predictions "
            "and accuracy."
            if reproducible
            else
            "The training runs produced different predictions "
            "or accuracy. Investigate the differences."
        ),
        "note": (
            "Artifact hash equality is reported separately. "
            "Different serialized model files can have different "
            "hashes even when predictions match."
        )
    }

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    # -----------------------------------------------------
    # DISPLAY RESULTS
    # -----------------------------------------------------

    print("\n" + "=" * 55)
    print("FRESH MODEL REPRODUCIBILITY EXPERIMENT")
    print("=" * 55)

    print("Run 1 Accuracy:",
          round(run_1["accuracy"] * 100, 2), "%")

    print("Run 2 Accuracy:",
          round(run_2["accuracy"] * 100, 2), "%")

    print("Predictions Match:", predictions_match)
    print("Accuracy Match:", accuracy_match)
    print("Artifact Hash Match:", artifact_hash_match)
    print("Experiment Result:", report["result"])
    print("Report Saved:", REPORT_PATH)

    print("=" * 55)

    return report


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":
    try:
        run_reproducibility_experiment()

    except (OSError, ValueError, KeyError) as error:
        print("\nExperiment failed:", error)