"""This moulde contains emthods or classes for pushing the best models into S3 Bucket"""

import sys
from src.object_detection.configuration.aws_storage_operations import S3Operation
from src.object_detection.entity.artifacts_entity import (ModelPusherArtifacts,
                                                          ModelTrainingArtifacts)
from src.object_detection.entity.config_entity import ModelPusherConfig
from src.object_detection.exception import ODISCException
from src.object_detection.logger import logging

class ModelPusher:
    """This class encapsulates the methods used for pushing the model in Storage"""
    def __init__(self, model_pusher_config: ModelPusherConfig, 
                 model_training_artifacts: ModelTrainingArtifacts, 
                 s3: S3Operation):
        self.model_pusher_config = model_pusher_config
        self.model_training_artifacts = model_training_artifacts
        self.s3 = s3

    def initiate_model_pusher(self) -> ModelPusherArtifacts:
        """This method is used for pushing the models into S3 Bucket"""
        try:
            logging.info("Inside initiate_model_pusher method of\
                         src.object_detection.model_pusher.ModelPusher")

            self.s3.upload_file(
                self.model_training_artifacts.trained_model_file_path,
                self.model_pusher_config.s3_model_key_path,
                self.model_pusher_config.model_bucket_name,
                remove=False
            )

            logging.info("Uploaded best model to S3 bucket")

            model_pusher_artifacts = ModelPusherArtifacts(
                bucket_name = self.model_pusher_config.model_bucket_name,
                s3_model_path = self.model_pusher_config.s3_model_key_path
            )

            logging.info("Completed execution of initiate_model_pusher method of\
                         src.object_detection.model_pusher.ModelPusher")

            return model_pusher_artifacts

        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error
