
# Model Reproducibility Registry

## 📌 Project Overview

The **Model Reproducibility Registry** is a Flask-based application designed to manage, track, validate, and audit machine learning model development and deployment.

The system maintains dataset versions, feature definitions, code versions, model artifacts, approval records, deployment information, and historical predictions in an SQLite database.

It helps improve model governance, reproducibility, artifact integrity, and auditability throughout the machine learning lifecycle.

## 🎯 Project Objectives

- Maintain dataset and feature version information.
- Track source code and model artifact versions.
- Manage model approval and deployment workflows.
- Record and validate historical predictions.
- Detect missing resources and dataset schema changes.
- Verify model artifact integrity using SHA-256 hashes.
- Conduct fresh model-retraining reproducibility experiments.
- Maintain audit records for model governance.

## 🚀 Key Features

### 1. Dataset Version Management

- Register and manage dataset versions.
- Store dataset metadata and schema information.
- Maintain dataset version history.
- Detect dataset schema changes.

### 2. Feature Management

- Register feature definitions.
- Associate features with feature versions.
- Maintain feature metadata for model development.

### 3. Code Version Management

- Register code versions and associated commit information.
- Maintain code version records for model traceability.

### 4. Model Artifact Management

- Register trained machine learning models.
- Store model artifact paths and metadata.
- Associate model artifacts with dataset and feature versions.
- Track model accuracy and artifact information.

### 5. Approval Workflow

The application supports role-based model approval workflows.

**Supported roles:**
- ML Engineer
- Auditor

Approval records are maintained in the registry for governance and traceability.

### 6. Deployment Management

- Register model deployment records.
- Track deployment information.
- Maintain deployment history in the database.

### 7. Historical Prediction Tracking

- Store historical prediction records.
- Associate predictions with registered model versions.
- Validate stored predictions against the registry's reproducibility checks.

### 8. Reproducibility Validation

The application provides reproducibility validation for registered model versions and historical predictions.

It includes:
- Historical prediction validation.
- Reproducibility experiment reporting.
- Model and version traceability.

### 9. Failure Testing

The application includes tests for missing registry resources, including:
- Missing dataset
- Missing code version
- Missing model

These tests help verify that the application detects the tested missing-resource conditions.

### 10. Dataset Schema Validation

The registry supports dataset schema registration and schema-drift detection.

It can identify changes in a dataset's registered schema and report whether schema drift is detected.

### 11. Artifact Integrity Verification

The application implements SHA-256-based model artifact integrity verification.

The feature:
- Calculates a model artifact's SHA-256 hash.
- Stores the hash in the registry database.
- Recalculates the hash during verification.
- Compares the current hash with the stored hash.
- Reports whether the artifact integrity check passes or fails.

### 12. Fresh Model-Retraining Reproducibility

A separate experiment script trains two models independently using the same dataset, feature configuration, and model parameters.

The experiment compares:
- Model accuracy
- Predictions
- Serialized artifact SHA-256 hashes

It generates a JSON report containing the experiment configuration, comparison results, and outcome.

## 📊 Dashboard

The application provides dashboard and management pages for viewing registry information and interacting with the model governance workflow.

Available pages include:

- Main Dashboard
- Dataset Management
- Model Management
- Approval Management
- Deployment Management
- Prediction Records
- Reproducibility Validation

## 👥 User Roles

### ML Engineer

The ML Engineer can perform model development and registry operations, including registering model-related information and working with approval and deployment workflows.

### Auditor

The Auditor role supports review and governance activities through the approval workflow and registry records.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application and machine learning logic |
| Flask | Web application framework and API |
| SQLite | Registry database |
| Pandas | Dataset loading and processing |
| Scikit-learn | Model training and evaluation |
| Joblib | Model artifact serialization |
| HTML | Web page structure |
| CSS | Web page styling |
| Git | Source code version control |

## 📁 Project Structure

```text
Model_Registry/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── integrity.py
│   └── ...
│
├── data/
│   └── dataset_v1.csv
│
├── models/
│   ├── train_model.py
│   ├── model_v1.pkl
│   ├── reproducibility_experiment.py
│   ├── reproducibility_run_1.pkl
│   ├── reproducibility_run_2.pkl
│   └── reproducibility_report.json
│
├── templates/
│   └── ...
│
├── static/
│   └── ...
│
├── model_registry.db
├── model_registry_backup.db
├── .gitignore
└── Readme.md
```

*Note: The structure above shows the main project files. Additional files and folders may exist in the application.*

## ⚙️ Installation and Setup

### Prerequisites

Install the following:

- Python
- pip
- Git
- Visual Studio Code (recommended)

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

### 2. Navigate to the Project Folder

```powershell
cd Model_Registry
```

### 3. Create a Virtual Environment

```powershell
python -m venv venv
```

### 4. Activate the Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

Install the required packages:

```powershell
pip install flask pandas scikit-learn joblib
```

### 6. Run the Application

Navigate to the backend directory:

```powershell
cd backend
```

Start the Flask application:

```powershell
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

Keep the terminal running while using the application.

## 🧪 Validation Summary

The current project database contains the following records:

| Component | Record Count |
|---|---:|
| Dataset Versions | 1 |
| Feature Definitions | 6 |
| Code Versions | 1 |
| Model Artifacts | 1 |
| Approvals | 2 |
| Deployments | 1 |
| Historical Predictions | 5 |
| Dataset Schema Records | 8 |
| Registry Rules | 5 |

These counts reflect the database state at the time of validation.

### 1. Historical Reproducibility Experiment

The recorded historical prediction experiment reported:

| Metric | Result |
|---|---:|
| Total Historical Predictions | 5 |
| Reproducible Predictions | 5 |
| Failed Predictions | 0 |
| Measured Reproducibility | 100% |
| Experiment Result | PASS |

This result reflects validation of stored historical predictions by the application. It does not independently demonstrate fresh model retraining.

### 2. Failure Testing

Three missing-resource failure tests were recorded:

| Test | Result |
|---|---|
| Missing Dataset | FAILED AS EXPECTED |
| Missing Code Version | FAILED AS EXPECTED |
| Missing Model | FAILED AS EXPECTED |

All three tests were reported as **FAILED AS EXPECTED**, indicating that the application detected the tested missing-resource conditions.

### 3. Dataset Schema Validation

The application supports dataset schema registration and schema-drift checking.

The following test was performed:

- An additional column was introduced to test schema change detection.
- The application detected the schema drift.
- The original dataset was restored.
- A subsequent schema check reported `NO DRIFT`.

**Status:** PASS — Schema drift detection was demonstrated successfully.

### 4. Artifact Integrity Verification

The registry's SHA-256-based artifact integrity verification was tested using `model_v1`.

The following operations were completed:

- **Hash Generation:** Calculated the SHA-256 hash of the registered model artifact.
- **Hash Storage:** Saved the calculated hash in the registry database.
- **Hash Verification:** Recalculated the hash and compared it with the stored hash.
- **Verification Result:** `REPRODUCIBLE: Artifact hash verified.`

**Model Version:** `model_v1`

**Verified SHA-256 Hash:**

```text
93d4d765be8ebe5a41ad2b20f2c2bb76d75f707044afe53d8daeb616bb6191f9
```

**Status:** PASS — The stored and recalculated artifact hashes matched during verification.

This confirms the integrity of the tested model artifact at verification time. It does not, by itself, establish that retraining will produce an identical model.

### 5. Fresh Model-Retraining Reproducibility

A fresh model-retraining experiment was conducted using two independent training runs with the same dataset, feature configuration, and model parameters.

**Experiment Configuration:**

| Parameter | Value |
|---|---|
| Dataset | `dataset_v1` |
| Feature Version | `feature_v1` |
| Model | `DecisionTreeClassifier` |
| Maximum Depth | 5 |
| Random State | 42 |
| Test Size | 20% |
| Training Runs | 2 |

**Experiment Results:**

| Metric | Run 1 | Run 2 |
|---|---:|---:|
| Model Accuracy | 98.8% | 98.8% |
| Predictions | Identical | Identical |
| Artifact SHA-256 | Matching | Matching |

**Validation Results:**

- **Predictions Match:** PASS
- **Accuracy Match:** PASS
- **Artifact Hash Match:** PASS
- **Experiment Result:** PASS

Both training runs produced identical predictions, accuracy, and serialized artifact hashes for the tested configuration and dataset.

**Experiment Report:**

`models/reproducibility_report.json`

**Status:** PASS — Fresh model-retraining reproducibility was successfully demonstrated for the tested configuration and dataset.

## 💾 Database

The application uses **SQLite** to store and manage model registry information.

The database contains the following tables and records:

- Dataset Versions
- Feature Definitions
- Code Versions
- Model Artifacts
- Approvals
- Deployments
- Historical Predictions
- Registry Rules
- Dataset Schemas

### Database Location

The configured database is located in the project root:

```text
model_registry.db
```

A separate database backup is maintained as:

```text
model_registry_backup.db
```

**Important:** Keep a backup of the database before making changes. The application is configured to use the root-level database, not the empty database file inside the `backend` folder.

## 🤖 Model Information

The project uses a **Decision Tree Classifier** for hospital risk-level prediction.

### Model Configuration

| Parameter | Value |
|---|---|
| Algorithm | Decision Tree Classifier |
| Maximum Depth | 5 |
| Random State | 42 |
| Training/Test Split | 80% / 20% |
| Dataset Version | `dataset_v1` |
| Feature Version | `feature_v1` |
| Model Version | `model_v1` |
| Recorded Accuracy | 98.8% |

### Input Features

The model uses the following six features:

1. Age
2. Gender
3. Blood Pressure
4. Glucose Level
5. Heart Rate
6. Symptom Score

**Target Variable:** `risk_level`

The dataset used in this project is a synthetic hospital-risk dataset. It is intended for project demonstration and software validation, not for real-world clinical diagnosis or treatment.

## 🔐 Model Governance and Auditability

The registry supports model governance through:

- Dataset and feature version tracking
- Code version registration
- Model artifact registration
- Role-based approval records
- Deployment tracking
- Historical prediction records
- Schema-drift detection
- Missing-resource failure testing
- SHA-256 artifact integrity verification
- Fresh model-retraining reproducibility experiments

These capabilities help maintain traceability and support auditing of the registered model lifecycle.

## 📈 Future Enhancements

Potential future improvements include:

- Automated model retraining and comparison through the web application
- Expanded audit logs and downloadable audit reports
- More comprehensive model validation metrics
- Automated dataset and model integrity checks
- Enhanced dashboard visualizations
- Additional role-based access controls
- Deployment monitoring and model performance tracking

## 👩‍💻 Author

**Deepika S**  
**Department:** B.Tech Information Technology  
**College:** Rathinam College, Coimbatore

## 📝 Conclusion

The **Model Reproducibility Registry** provides a Flask-based platform for tracking and validating machine learning model lifecycle information.

It brings together dataset and feature versioning, code and model registration, approval workflows, deployment tracking, historical prediction validation, schema-drift detection, artifact integrity verification, and fresh model-retraining reproducibility experiments.

The tested features demonstrate the application's ability to maintain registry records, detect selected failure conditions, verify artifact integrity, and reproduce matching model results under the tested configuration.

The project provides a foundation for improving machine learning traceability, reproducibility, and governance.