from dataclasses import dataclass
from typing import Optional


@dataclass
class DatasetVersion:
    dataset_version: str
    dataset_name: str
    file_path: Optional[str] = None
    record_count: Optional[int] = None


@dataclass
class FeatureDefinition:
    feature_version: str
    feature_name: str
    definition: str
    data_type: Optional[str] = None


@dataclass
class CodeVersion:
    code_version: str
    commit_hash: str
    repository: Optional[str] = None


@dataclass
class ModelArtifact:
    model_version: str
    model_name: str
    artifact_path: Optional[str] = None
    algorithm: Optional[str] = None
    parameters: Optional[str] = None


@dataclass
class Approval:
    model_version: str
    approved_by: str
    role: str
    approval_status: str
    comments: Optional[str] = None


@dataclass
class Deployment:
    deployment_version: str
    model_version: str
    environment: str
    deployed_by: Optional[str] = None
    deployment_status: str = "PENDING"