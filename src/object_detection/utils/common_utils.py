"""This module contains all the common utils"""

import sys
import base64
import yaml

from src.object_detection.exception import ODISCException
from src.object_detection.logger import logging


def read_yaml_file(file_path: str) -> dict:
    """This function is used to load and read the yaml file"""
    try:
        with open(file_path, "rb") as yaml_file:
            logging.info("Read yaml file successfully")
            return yaml.safe_load(yaml_file)

    except Exception as error:
        raise ODISCException(error, sys) from error


def decode_image(image_string, file_name):
    """This function is used to decode the image string to image data"""
    img_data = base64.b64decode(image_string)
    with open("./data/" + file_name, "wb") as image_file:
        image_file.write(img_data)
        image_file.close()


def encode_image_to_base64(image_path):
    """This function encodes the image into base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read())
