"""This module includes all the triggers for each pipeline"""

import sys
from src.object_detection.logger import logging
from src.object_detection.exception import ODISCException
from src.object_detection.configuration.aws_storage_operations import S3Operation
from src.object_detection.components.data_ingestion import DataIngestion
from src.object_detection.components.data_validation import DataValidation
from src.object_detection.components.model_trainer import ModelTraining
from src.object_detection.components.model_pusher import ModelPusher

from src.object_detection.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    ModelTrainingConfig,
    ModelPusherConfig,
)

from src.object_detection.entity.artifacts_entity import (
    DataIngestionArtifacts,
    DataValidationArtifacts,
    ModelTrainingArtifacts,
    ModelPusherArtifacts,
)


class TrainingPipeline:
    """This class and methods encapsulates all the methods that are used for
    Model Training pipeline"""

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.model_training_config = ModelTrainingConfig()
        self.model_pusher_config = ModelPusherConfig()
        self.s3_operations = S3Operation()

    def start_data_ingestion(self) -> DataIngestionArtifacts:
        """This method basically starts the data ingestion process when
        triggered by run_pipeline"""

        try:
            logging.info(
                " Inside the start_data_ingestion method of \
                         src.object_detection.pipeline.TrainingPipeline class"
            )
            logging.info("Fetching data from S3 Bucket URL")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Fetched the data from URL")
            logging.info(
                "Completed execution of the start_data_ingestion method of \
                         src.object_detection.pipeline.TrainingPipeline class"
            )

            return data_ingestion_artifact
        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error

    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifacts
    ) -> DataValidationArtifacts:
        """This method starts the data validation process when triggered by run_pipeline"""
        try:
            logging.info(
                "Inside the start_data_validation method of\
                src.object_detection.pipeline.TrainingPipeline class"
            )

            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")

            logging.info(
                "Completed executing the start_data_validation method of \
                         src.object_detection.pipeline.TrainingPipeline class"
            )

            return data_validation_artifact
        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error

    def start_model_training(self) -> ModelTrainingArtifacts:
        """This method starts the model training pipeline"""
        try:
            logging.info(
                "Inside the start_model_training method of \
                         src.object_detection.pipeline.TrainingPipeline class"
            )

            model_training = ModelTraining(
                model_training_config=self.model_training_config
            )

            model_training_artifacts = model_training.initite_model_training()

            logging.info(
                "Completed execution of the start_model_training method of \
                         src.object_detection.pipeline.TrainingPipeline class"
            )

            return model_training_artifacts
        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error

    def start_model_pusher(
        self, model_training_artifacts: ModelTrainingArtifacts, s3_storage: S3Operation
    ) -> ModelPusherArtifacts:
        """This method starts the model training pipeline"""
        try:
            logging.info(
                "Inside the start_model_pusher method of \
                         src.object_detection.pipeline.TrainingPipeline class"
            )

            model_pusher = ModelPusher(
                model_pusher_config=self.model_pusher_config,
                model_training_artifacts=model_training_artifacts,
                s3_storage=s3_storage,
            )

            model_pusher_artifacts = model_pusher.initiate_model_pusher()

            logging.info(
                "Completed execution of the start_model_pusher method of \
                         src.object_detection.pipeline.TrainingPipeline class"
            )

            return model_pusher_artifacts
        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error

    def run_pipeline(self) -> None:
        """This method basically call all the methods and object to run each pipeline"""
        try:
            logging.info(
                "Inside the run_pipeline method of \
                         src.object_detection.pipeline.TrainingPipeline class"
            )

            data_ingestion_artifact = self.start_data_ingestion()

            logging.info(
                "Completed start_data_ingestion method of \
                         src.object_detection.pipeline.TrainingPipeline class"
            )

            data_validation_artifacts = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )

            logging.info(
                "Completed start_data_validation method of \
                         src.object_detection.pipeline.TrainingPipeline class"
            )

            if data_validation_artifacts.validation_status:
                model_training_artifacts = self.start_model_training()

                logging.info(
                    "Completed start_model_training method of \
                         src.object_detection.pipeline.TrainingPipeline class"
                )

                model_pusher_artifact = self.start_model_pusher(
                    model_training_artifacts=model_training_artifacts,
                    s3_storage=self.s3_operations,
                )

                logging.info(
                    "Completed start_model_pusher method of \
                         src.object_detection.pipeline.TrainingPipeline class"
                )

                logging.info(f"model_pusher_artifact - {model_pusher_artifact}")

            else:
                raise ValueError(
                    "Some issue in Data Validation Please check and validate"
                )

        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error
