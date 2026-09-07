import pandas as pd
import random

random.seed(42)

data = []

for i in range(1, 5001):
    age = random.randint(18, 80)
    gender = random.choice(["Male", "Female"])
    blood_pressure = random.randint(90, 180)
    glucose_level = random.randint(70, 250)
    heart_rate = random.randint(55, 120)
    symptom_score = random.randint(0, 10)

    # Synthetic target
    if (
        blood_pressure >= 140
        or glucose_level >= 180
        or heart_rate >= 100
        or symptom_score >= 7
    ):
        risk_level = "High"
    elif (
        blood_pressure >= 120
        or glucose_level >= 120
        or heart_rate >= 85
        or symptom_score >= 4
    ):
        risk_level = "Medium"
    else:
        risk_level = "Low"

    data.append([
        f"P{i:03d}",
        age,
        gender,
        blood_pressure,
        glucose_level,
        heart_rate,
        symptom_score,
        risk_level
    ])

columns = [
    "patient_id",
    "age",
    "gender",
    "blood_pressure",
    "glucose_level",
    "heart_rate",
    "symptom_score",
    "risk_level"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("data/dataset_v1.csv", index=False)

print("dataset_v1.csv created successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print(df.head())