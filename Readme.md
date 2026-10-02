# 🤖 Model Reproducibility Registry

## 📌 Project Overview

The Model Reproducibility Registry is a Machine Learning Governance System designed to track, validate, reproduce, and audit Machine Learning models.

The system maintains version information for datasets, features, code, models, approvals, deployments, and historical predictions. This helps ensure that Machine Learning predictions can be traced back to the resources and versions used during prediction.

The project provides a dynamic dashboard with clickable cards that display detailed records for each component of the Machine Learning lifecycle.

---

## 🎯 Project Objectives

* Track Dataset Versions
* Track Feature Definitions
* Track Code Versions
* Register Model Artifacts
* Record Model Approvals
* Track Model Deployments
* Store Historical Predictions
* Validate Prediction Reproducibility
* Perform Audit Tracking
* Maintain Machine Learning Governance

---

## 🚀 Features

### 📁 Dataset Versioning

Stores dataset version, dataset name, file path, record count, and creation date.

### 🔍 Feature Tracking

Tracks feature definitions used by Machine Learning models.

Example features:

* Age
* Gender
* Blood Pressure
* Glucose Level
* Heart Rate
* Symptom Score

### 💻 Code Versioning

Tracks:

* Code Version
* Commit Hash
* Repository

### 🤖 Model Registry

Stores:

* Model Version
* Model Name
* Artifact Path
* Algorithm
* Parameters

### ✅ Model Approval

Records:

* Model Version
* Approved By
* Role
* Approval Status
* Approval Date
* Comments

### 🚀 Deployment Tracking

Tracks:

* Deployment Version
* Model Version
* Environment
* Deployed By
* Deployment Status
* Deployment Date

### 📊 Historical Predictions

Stores prediction records along with:

* Dataset Version
* Feature Version
* Code Version
* Model Version
* Deployment Version
* Reproducibility Status

### ♻️ Reproducibility Validation

The system validates historical predictions using:

* Dataset Version
* Feature Version
* Code Version
* Model Version

Predictions are marked as:

* REPRODUCIBLE
* FAILED

### 🧪 Failure Testing

The system includes tests for missing registered resources, such as datasets, code versions, and models. These tests check whether expected failures are detected.

---

## 🖥️ Dashboard

The interactive dashboard contains clickable cards for:

* 📁 Dataset Versions
* 🤖 Model Artifacts
* ✅ Approvals
* 🚀 Deployments
* 📊 Historical Predictions
* ♻️ Reproducible Predictions

Each card opens a detailed page displaying the corresponding records.

---

## 👥 Project Roles

### 👨‍💻 ML Engineer

Responsible for:

* Model Development
* Model Registration
* Deployment
* Prediction Tracking

### 🔍 Auditor

Responsible for:

* Model Approval
* Audit Verification
* Reproducibility Validation
* Governance Tracking

---

## 🛠️ Technologies Used

* Python
* Flask
* SQLite
* HTML
* CSS
* Jinja Templates
* Git
* GitHub
* Pandas
* Scikit-learn

---

## 📂 Project Structure

```text
Model_Registry/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   └── integrity.py
│
├── data/
│   └── dataset_v1.csv
│
├── models/
│   ├── model_v1.pkl
│   └── train_model.py
│
├── templates/
│   ├── dashboard.html
│   ├── datasets.html
│   ├── models.html
│   ├── approvals.html
│   ├── deployments.html
│   ├── predictions.html
│   └── reproducible.html
│
├── fix_feature_schema.py
├── model_registry.db
├── model_registry_backup.db
└── Readme.md
```

---

## ⚙️ Setup and Run

### 1. Prerequisites

Make sure Python and pip are installed on your system.

### 2. Install Dependencies

Open a terminal in the project folder and install the required packages:

```bash
pip install flask pandas scikit-learn
```

If the application uses additional packages, install those as required by the project's imports.

### 3. Navigate to the Backend Folder

```bash
cd backend
```

### 4. Run the Application

```bash
python app.py
```

### 5. Open the Dashboard

Open your web browser and visit:

```text
http://127.0.0.1:5000
```

Keep the terminal running while using the application.

---

## 🧪 Validation Summary

The current project database contains the following records:

| Component              | Record Count |
| ---------------------- | -----------: |
| Dataset Versions       |            1 |
| Feature Definitions    |            6 |
| Code Versions          |            1 |
| Model Artifacts        |            1 |
| Approvals              |            2 |
| Deployments            |            1 |
| Historical Predictions |            5 |
| Dataset Schema Records |            8 |
| Registry Rules         |            5 |

### Reproducibility Experiment

The recorded reproducibility experiment reported:

* Total Historical Predictions: 5
* Reproducible Predictions: 5
* Failed Predictions: 0
* Measured Reproducibility: 100%
* Experiment Result: PASS

This result reflects validation of stored historical predictions by the application. It does not independently demonstrate a fresh model-retraining experiment.

### Failure Testing

Three missing-resource failure tests were recorded:

* Missing Dataset
* Missing Code Version
* Missing Model

All three were reported as **FAILED AS EXPECTED**, indicating that the application detected the tested missing-resource conditions.

### Dataset Schema Validation

The application includes dataset schema registration and schema-drift checking. An added-column test detected schema drift, and the original dataset was restored and subsequently reported no drift.

## 💾 Database

The application uses SQLite to store:

- Dataset Versions
- Feature Definitions
- Code Versions
- Model Artifacts
- Approvals
- Deployments
- Historical Predictions
- Registry Rules
- Dataset Schemas

The configured database is located in the project root:

`model_registry.db`

A separate database backup is maintained as:

`model_registry_backup.db`

**Important:** Keep a backup of the database before making changes. The application is configured to use the root-level database, not the empty database file inside the backend folder.

## 📈 Model Information

The project includes a Hospital Risk Prediction Model trained using a Decision Tree Classifier.

The model uses the following input features:

* Age
* Gender
* Blood Pressure
* Glucose Level
* Heart Rate
* Symptom Score

The model configuration includes:

* Algorithm: Decision Tree Classifier
* Maximum Depth: 5
* Random State: 42
* Train-Test Split: 80:20

The registered model artifact is stored at:

```text
models/model_v1.pkl
```

The model's registered accuracy is 98.8%. This is the project's recorded metric and should be interpreted in the context of its dataset and evaluation method.

**Dataset note:** The hospital-risk dataset is a project dataset and should not be represented as real patient data unless independently verified.

---

## 🔐 Model Governance

The registry supports model lifecycle governance through:

* Dataset and feature version tracking
* Code and model artifact registration
* Model approval records
* Deployment tracking
* Historical prediction records
* Reproducibility validation
* Audit summaries
* Failure testing

These capabilities help maintain traceability and accountability across the model lifecycle.

---

## 👩‍🎓 Author

**Deepika S**
B.Tech Information Technology
Rathinam College, Coimbatore

---

## 📌 Conclusion

The Model Reproducibility Registry provides a centralized application for tracking machine learning resources, model versions, approvals, deployments, and historical predictions.

It demonstrates how version tracking, reproducibility checks, audit records, and failure testing can be incorporated into a machine learning governance workflow.
