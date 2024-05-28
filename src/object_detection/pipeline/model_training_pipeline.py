"""This module includes all the triggers for each pipeline"""

import sys
from src.object_detection.logger import logging
from src.object_detection.exception import ODISCException
from src.object_detection.configuration.aws_storage_operations import S3Operation
from src.object_detection.components.data_ingestion import DataIngestion
from src.object_detection.components.data_validation import DataValidation



from src.object_detection.entity.config_entity import (DataIngestionConfig,
                                                       DataValidationConfig,)


from src.object_detection.entity.artifacts_entity import (DataIngestionArtifact,
                                                          DataValidationArtifact)


class TrainingPipeline:
    """This class and methods encapsulates all the methods that are used for 
    Model Training pipeline"""
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        # self.model_trainer_config = ModelTrainerConfig()
        # self.model_pusher_config = ModelPusherConfig()
        self.s3_operations = S3Operation()


    def start_data_ingestion(self)-> DataIngestionArtifact:
        """This method basically starts the data ingestion process when 
        triggered by run_pipeline"""

        try:
            logging.info(" Inside the start_data_ingestion method of \
                         src.object_detection.pipeline.TrainingPipeline class"
            )
            logging.info("Fetching data from S3 Bucket URL")

            data_ingestion = DataIngestion(
                data_ingestion_config =  self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Fetched the data from URL")
            logging.info("Completed execution of the start_data_ingestion method of \
                         src.object_detection.pipeline.TrainingPipeline class"
            )

            return data_ingestion_artifact

        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error


    def start_data_validation(self, 
                              data_ingestion_artifact: DataIngestionArtifact
                              ) -> DataValidationArtifact:
        """This method starts the data validation pipeline"""
        try:
            logging.info("Inside the start_data_validation method of \
                         src.object_detection.pipeline.TrainingPipeline class")

            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")

            logging.info("Completed executing the start_data_validation method of \
                         src.object_detection.pipeline.TrainingPipeline class")

            return data_validation_artifact
        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error


    def run_pipeline(self) -> None:
        """This method basically call all the methods and object to run each pipeline"""
        try:
            data_ingestion_artifact = self.start_data_ingestion()

            print(data_ingestion_artifact)

        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error
