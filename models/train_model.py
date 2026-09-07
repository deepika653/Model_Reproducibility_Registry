import pandas as pd
import joblib

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

MODEL_PATH = BASE_DIR / "models" / "model_v1.pkl"


# ---------------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# ---------------------------------------------------------
# FEATURES AND TARGET
# ---------------------------------------------------------

feature_columns = [
    "age",
    "gender",
    "blood_pressure",
    "glucose_level",
    "heart_rate",
    "symptom_score"
]

X = df[feature_columns].copy()
y = df["risk_level"]


# ---------------------------------------------------------
# ENCODE GENDER
# ---------------------------------------------------------

gender_encoder = LabelEncoder()

X["gender"] = gender_encoder.fit_transform(X["gender"])


# ---------------------------------------------------------
# TRAIN / TEST SPLIT
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ---------------------------------------------------------
# CREATE MODEL
# ---------------------------------------------------------

model = DecisionTreeClassifier(
    max_depth=5,
    random_state=42
)


# ---------------------------------------------------------
# TRAIN MODEL
# ---------------------------------------------------------

model.fit(X_train, y_train)


# ---------------------------------------------------------
# TEST MODEL
# ---------------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", round(accuracy * 100, 2), "%")


# ---------------------------------------------------------
# SAVE MODEL ARTIFACT
# ---------------------------------------------------------

model_data = {
    "model": model,
    "gender_encoder": gender_encoder,
    "feature_columns": feature_columns,
    "accuracy": accuracy,
    "dataset_version": "dataset_v1",
    "feature_version": "feature_v1"
}

joblib.dump(model_data, MODEL_PATH)

print("Model saved successfully!")
print("Model version: model_v1")
print("Model path:", MODEL_PATH)