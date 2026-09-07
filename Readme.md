# 🤖 Model Reproducibility Registry

## 📌 Project Overview

The Model Reproducibility Registry is a Machine Learning Governance System designed to track, validate, reproduce, and audit Machine Learning models.

The system maintains version information for datasets, features, code, models, approvals, deployments, and historical predictions. This helps ensure that Machine Learning predictions can be traced back to the exact resources and versions used during prediction.

The project provides a dynamic dashboard with clickable cards that display detailed records for each component of the Machine Learning lifecycle.

---

## 🎯 Project Objectives

- Track Dataset Versions
- Track Feature Definitions
- Track Code Versions
- Register Model Artifacts
- Record Model Approvals
- Track Model Deployments
- Store Historical Predictions
- Validate Prediction Reproducibility
- Perform Audit Tracking
- Maintain Machine Learning Governance

---

## 🚀 Features

### 📁 Dataset Versioning

Stores dataset version, dataset name, file path, record count, and created date.

### 🔍 Feature Tracking

Tracks feature definitions used by Machine Learning models.

Example features:

- Age
- Gender
- Blood Pressure
- Glucose Level
- Heart Rate
- Symptom Score

### 💻 Code Versioning

Tracks:

- Code Version
- Commit Hash
- Repository

### 🤖 Model Registry

Stores:

- Model Version
- Model Name
- Artifact Path
- Algorithm
- Parameters

### ✅ Model Approval

Records:

- Model Version
- Approved By
- Role
- Approval Status
- Approval Date
- Comments

### 🚀 Deployment Tracking

Tracks:

- Deployment Version
- Model Version
- Environment
- Deployed By
- Deployment Status
- Deployment Date

### 📊 Historical Predictions

Stores prediction records along with:

- Dataset Version
- Feature Version
- Code Version
- Model Version
- Deployment Version
- Reproducibility Status

### ♻️ Reproducibility Validation

The system validates historical predictions using:

- Dataset Version
- Feature Version
- Code Version
- Model Version

Predictions are marked as:

- REPRODUCIBLE
- FAILED

---

## 🖥️ Dashboard

The interactive dashboard contains clickable cards for:

- 📁 Dataset Versions
- 🤖 Model Artifacts
- ✅ Approvals
- 🚀 Deployments
- 📊 Historical Predictions
- ♻️ Reproducible Predictions

Each card opens a detailed page displaying the corresponding records.

---

## 👥 Project Roles

### 👨‍💻 ML Engineer

Responsible for:

- Model Development
- Model Registration
- Deployment
- Prediction Tracking

### 🔍 Auditor

Responsible for:

- Model Approval
- Audit Verification
- Reproducibility Validation
- Governance Tracking

---

## 🛠️ Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja Templates
- Git
- GitHub

---

## 📂 Project Structure

```text
Model_Registry/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   └── models.py
│
├── data/
│   └── dataset_v1.csv
│
├── models/
│   └── model_v1.pkl
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
└── README.md