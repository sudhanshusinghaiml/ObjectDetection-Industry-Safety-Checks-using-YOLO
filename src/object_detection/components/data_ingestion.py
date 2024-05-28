"""This module includes all objects for Data Ingestion"""

import os
import sys
from src.object_detection.logger import logging
from src.object_detection.exception import ODISCException
from src.object_detection.entity.config_entity import DataIngestionConfig
from src.object_detection.entity.artifacts_entity import DataIngestionArtifacts
from src.object_detection.configuration.aws_storage_operations import S3Operation
from src.object_detection.constants import DATA_BUCKET_NAME


class DataIngestion:
    """This class encapsulates all the methods related to Data Ingestion"""
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
            self.s3 = S3Operation()
        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error


    def download_data(self)-> str:
        """ This method is used to download the data from s3 """
        try:
            zip_download_dir = self.data_ingestion_config.data_ingestion_directory
            os.makedirs(zip_download_dir, exist_ok=True)

            logging.info(f"Downloading data from s3 into file {zip_download_dir}")

            zip_file_path = os.path.join(zip_download_dir, self.data_ingestion_config.s3_data_name)

            self.s3.download_object(key= self.data_ingestion_config.s3_data_name, 
                                    bucket_name=DATA_BUCKET_NAME, filename = zip_file_path)
            logging.info(f"Downloaded data from s3 into file {zip_file_path}")
            return zip_file_path

        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error


    def extract_zip_file(self, zip_file_path: str)-> str:
        """This method is used to extract all files from zip_file_path"""
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.system(f"unzip {zip_file_path} -d {feature_store_path}")

            return feature_store_path

        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error


    def initiate_data_ingestion(self)-> DataIngestionArtifacts:
        """This method is used to initiate data ingestion"""
        logging.info("Inside initiate_data_ingestion method of \
                     src.object_detection.components.Data_Ingestion class")
        try:
            zip_file_path = self.download_data()
            feature_store_path = self.extract_zip_file(zip_file_path)
            logging.info(f"unzipped the file into {zip_file_path}")

            data_ingestion_artifact = DataIngestionArtifacts(
                data_zip_file_path = zip_file_path,
                feature_store_path = feature_store_path
            )

            logging.info("Completed executing initiate_data_ingestion method of \
                         src.object_detection.components.Data_Ingestion class")

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact
        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error
