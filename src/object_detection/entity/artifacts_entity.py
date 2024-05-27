"""This module includes all the artifacts for each stage of pipeline"""

from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    """This class includes artifacts for Data Ingestion"""

    data_zip_file_path: str
    feature_store_path: str


@dataclass
class DataValidationArtifact:
    """This class includes artifacts for Data Ingestion"""

    validation_status: bool


@dataclass
class ModelTrainerArtifact:
    """This class includes artifacts for Model Trainer"""

    trained_model_file_path: str


@dataclass
class ModelPusherArtifacts:
    """This class includes artifacts for Model Pusher"""

    bucket_name: str
    s3_model_path: str
