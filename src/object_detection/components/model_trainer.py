"""This module includes class and methods for model training"""

import os
import shutil
import sys
from datetime import datetime
from six.moves import urllib  # type: ignore
from src.object_detection.logger import logging
from src.object_detection.exception import ODISCException
from src.object_detection.constants import (
    DATA_INGESTION_S3_DATA_NAME,
    DATA_VALIDATION_ALL_REQUIRED_FILES,
)
from src.object_detection.entity.config_entity import ModelTrainingConfig
from src.object_detection.entity.artifacts_entity import ModelTrainingArtifacts


class ModelTraining:
    """This calss encapsulates the methods for model training"""

    def __init__(self, model_training_config: ModelTrainingConfig):
        self.model_training_config = model_training_config

    def initite_model_training(self) -> ModelTrainingArtifacts:
        """This method initates the model training"""
        try:
            logging.info(
                "Inside initite_model_training method of\
                         src.object_detection.model_trainer.ModelTraining"
            )

            logging.info(f"Present Working directory -{os.getcwd()}")

            logging.info("Creating model_training directory")

            os.makedirs(self.model_training_config.model_trainer_data_directory, exist_ok=True)

            os.system(f"unzip {DATA_INGESTION_S3_DATA_NAME} -d \
                      {self.model_training_config.model_trainer_data_directory}")

            os.system(f"rm {DATA_INGESTION_S3_DATA_NAME}")

            # Prepare image path in the text file
            training_image_path= os.path.join(
                self.model_training_config.model_trainer_data_directory, "images", "train")
            validation_image_path= os.path.join(
                self.model_training_config.model_trainer_data_directory, "images", "val")

            training_image_reference = os.path.join(
                self.model_training_config.model_trainer_data_directory,
                DATA_VALIDATION_ALL_REQUIRED_FILES[3]
                )

            validation_image_reference = os.path.join(
                self.model_training_config.model_trainer_data_directory,
                DATA_VALIDATION_ALL_REQUIRED_FILES[4]
                )

            # Training Images
            with open(
                training_image_reference, "a+", encoding="utf-8"
            ) as file:
                image_list = os.listdir(training_image_path)
                for image in image_list:
                    file.write(os.path.join(training_image_path, image + "\n"))

            logging.info(f"Updated/Added training image path in {training_image_reference}")

            # Validation Images
            with open(validation_image_reference, "a+", encoding="utf-8") as file:
                image_list = os.listdir(validation_image_path)
                for image in image_list:
                    file.write(os.path.join(validation_image_path, image + "\n"))

            logging.info(f"Updated/Added validation image path in {validation_image_reference}")

            # Downloading COCO starting checkpoint
            url = self.model_training_config.weight_name
            file_name = os.path.basename(url)
            urllib.request.urlretrieve(url, os.path.join("yolov7", file_name))

            logging.info(f"Present working directory is - {os.getcwd()}")

            logging.info(f"Model Training started - {datetime.now()}")

            # Model Training
            # os.system(
            #     f"python yolov7/train.py \
            #     --batch {self.model_training_config.batch_size} \
            #     --cfg yolov7/cfg/training/custom_yolov7.yaml \
            #     --epochs {self.model_training_config.no_epochs} \
            #     --data yolov7/data/custom.yaml --weights /yolov7/yolov7.pt\
            #     "
            # )

            os.system(f"python yolov7/train.py --batch {self.model_training_config.batch_size} --cfg yolov7/cfg/training/custom_yolov7.yaml --epochs {self.model_training_config.no_epochs} --data yolov7/data/custom.yaml --weights yolov7/yolov7.pt ")

            logging.info(f"Model Training completed - {datetime.now()}")
            logging.info(f"Present working directory is - {os.getcwd()}")

            # os.system("cp yolov7/runs/train/exp/weights/best.pt yolov7/")
            try:
                shutil.copy("yolov7/runs/train/exp/weights/best.pt", "yolov7/")
                logging.info("Copied best models in yolov7/best.pt")
            except FileNotFoundError as error:
                logging.error(f"File not found: {error}")

            os.makedirs(self.model_training_config.model_trainer_directory, exist_ok=True)

            try:
                shutil.copy("yolov7/runs/train/exp/weights/best.pt", 
                            self.model_training_config.model_trainer_directory)
                logging.info("Copied best models in yolov7/best.pt")
            except FileNotFoundError as error:
                logging.error(f"File not found: {error}")

            logging.info(f"Copied best models in \
                         {self.model_training_config.model_trainer_directory}")

            # os.system("rm -rf yolov7/runs")
            # os.system("rm -rf images")
            # os.system("rm -rf labels")
            # os.system("rm -rf classes.names")
            # os.system("rm -rf train.txt")
            # os.system("rm -rf val.txt")
            # os.system("rm -rf train.cache")
            # os.system("rm -rf val.cache")

            model_training_artifact = ModelTrainingArtifacts(
                trained_model_file_path= self.model_training_config.best_trained_model_path
            )

            logging.info(
                "Successfully completed initiate_model_trainer method of \
                         src.object_detection.model_trainer.ModelTraining class"
            )

            return model_training_artifact

        except Exception as error:
            logging.error(error)
            raise ODISCException(error, sys) from error
