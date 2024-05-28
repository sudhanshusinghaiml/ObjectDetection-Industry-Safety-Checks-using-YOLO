"""This module includes the classes and methods for Data Validation"""
import os
import shutil
import sys
from src.object_detection.logger import logging
from src.object_detection.exception import ODISCException
from src.object_detection.entity.config_entity import DataValidationConfig
from src.object_detection.entity.artifacts_entity import (DataIngestionArtifact,
                                                          DataValidationArtifact)



class DataValidation:
    """This class encapuslates the methods associated to data validations"""
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error


    def validate_if_all_file_exists(self) -> bool:
        """This method is used to validate if all the required files exists in 
        featured store path"""
        try:
            validation_status = None

            files = os.listdir(self.data_ingestion_artifact.feature_store_path)

            for file in files:
                if file not in self.data_validation_config.required_file_list:
                    validation_status = False
                    os.makedirs(self.data_validation_config.data_validation_directory,
                                exist_ok=True)
                    with open(self.data_validation_config.valid_status_file_directory,
                              "w", encoding="utf-8") as file_dir:
                        file_dir.write(f"Validation status: {validation_status}")
                else:
                    validation_status = True
                    os.makedirs(self.data_validation_config.data_validation_directory,
                                exist_ok=True)
                    with open(self.data_validation_config.valid_status_file_directory,
                              "w", encoding="utf-8") as file_dir:
                        file_dir.write(f"Validation status: {validation_status}")

            return validation_status
        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error


    def initiate_data_validation(self) -> DataValidationArtifact:
        """This method is used to initiate the datavalidation process"""
        try:
            logging.info("Inside initiate_data_validation method of \
                         src.object_detection.components.data_validation class")
            status = self.validate_if_all_file_exists()
            data_validation_artifact = DataValidationArtifact(
                validation_status = status
            )

            logging.info("Executed validate_if_all_file_exists method of \
                         src.object_detection.components.data_validation class")

            if status:
                shutil.copy(self.data_ingestion_artifact.data_zip_file_path, os.getcwd())

            logging.info("Completed execution of initiate_data_validation method of \
                         src.object_detection.components.data_validation class")

            return data_validation_artifact
        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error
