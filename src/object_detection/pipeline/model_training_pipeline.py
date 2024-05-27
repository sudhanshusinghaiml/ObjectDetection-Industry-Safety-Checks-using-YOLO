"""This module includes all the triggers for each pipeline"""

import sys
from src.object_detection.logger import logging
from src.object_detection.exception import ODISCException
from src.object_detection.configuration.aws_storage_operations import S3Operation
from src.object_detection.components.data_ingestion import DataIngestion


from src.object_detection.entity.config_entity import (DataIngestionConfig)


from src.object_detection.entity.artifacts_entity import (DataIngestionArtifact)


class TrainPipeline:
    """This class and methods encapsulates all the methods that are used for Model Training pipeline"""
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        # self.data_validation_config = DataValidationConfig()
        # self.model_trainer_config = ModelTrainerConfig()
        # self.model_pusher_config = ModelPusherConfig()
        self.s3_operations = S3Operation()


    
    def start_data_ingestion(self)-> DataIngestionArtifact:
        """This method basically starts the data ingestion process when triggered by run_pipeline"""

        try: 
            logging.info(
                "Entered the start_data_ingestion method of TrainPipeline class"
            )
            logging.info("Getting the data from URL")

            data_ingestion = DataIngestion(
                data_ingestion_config =  self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the data from URL")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise ODISCException(e, sys) from e
        

    def run_pipeline(self) -> None:
        """This method basically call all the methods and object to run each pipeline"""
        try:
            data_ingestion_artifact = self.start_data_ingestion()

            print(data_ingestion_artifact)


        except Exception as e:
            raise ODISCException(e, sys) from e
