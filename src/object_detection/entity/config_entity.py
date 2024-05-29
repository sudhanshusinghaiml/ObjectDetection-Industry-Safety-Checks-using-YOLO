"""This module contains all the dataclass and configurations"""

import os
from dataclasses import dataclass
from datetime import datetime
from src.object_detection.constants import (
    ARTIFACTS_DIR,
    DATA_INGESTION_DIR_NAME,
    DATA_INGESTION_FEATURE_STORE_DIR,
    DATA_VALIDATION_ALL_REQUIRED_FILES,
    DATA_VALIDATION_DIR_NAME,
    DATA_INGESTION_S3_DATA_NAME,
    DATA_VALIDATION_STATUS_FILE,
    MODEL_TRAINER_DIR_NAME,
    MODEL_BUCKET_NAME,
    MODEL_TRAINER_BATCH_SIZE,
    MODEL_TRAINER_NO_EPOCHS,
    MODEL_TRAINER_PRETRAINED_WEIGHT_URL,
    S3_MODEL_NAME,
    BEST_MODEL_NAME,
)


TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class TrainingPipelineConfig:
    """This dataclass contains the Training Pipeline Config"""

    artifacts_directory: str = os.path.join(ARTIFACTS_DIR, TIMESTAMP)


training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    """This dataclass contains the Data Ingestion Config"""

    data_ingestion_directory: str = os.path.join(
        training_pipeline_config.artifacts_directory, DATA_INGESTION_DIR_NAME
    )
    feature_store_file_path: str = os.path.join(
        data_ingestion_directory, DATA_INGESTION_FEATURE_STORE_DIR
    )
    s3_data_name = DATA_INGESTION_S3_DATA_NAME


@dataclass
class DataValidationConfig:
    """This dataclass contains the Data Validation Config"""

    data_validation_directory: str = os.path.join(
        training_pipeline_config.artifacts_directory, DATA_VALIDATION_DIR_NAME
    )
    valid_status_file_directory: str = os.path.join(
        data_validation_directory, DATA_VALIDATION_STATUS_FILE
    )
    required_file_list = DATA_VALIDATION_ALL_REQUIRED_FILES


@dataclass
class ModelTrainingConfig:
    """This dataclass contains the Model Training Config"""

    model_trainer_data_directory: str = os.path.join(
        ARTIFACTS_DIR, MODEL_TRAINER_DIR_NAME
    )

    model_trainer_directory: str = os.path.join(
        training_pipeline_config.artifacts_directory, MODEL_TRAINER_DIR_NAME
    )
    best_trained_model_path: str = os.path.join(model_trainer_directory, BEST_MODEL_NAME)
    weight_name = MODEL_TRAINER_PRETRAINED_WEIGHT_URL
    no_epochs = MODEL_TRAINER_NO_EPOCHS
    batch_size = MODEL_TRAINER_BATCH_SIZE


@dataclass
class ModelPusherConfig:
    """This dataclass contains the Model Pusher Config"""

    model_bucket_name: str = MODEL_BUCKET_NAME
    s3_model_key_path: str = S3_MODEL_NAME
