"""
This module contains the code that reads the input data from webapp
transforms it as input to prediction pipeline
                OR
It triggers all the training pipeline
"""

import os
from flask import Flask, request, jsonify, render_template,Response
from flask_cors import cross_origin
from src.object_detection.pipeline.model_training_pipeline import TrainingPipeline
from src.object_detection.exception import ODISCException
from src.object_detection.utils.common_utils import decode_image, encode_image_to_base64


# 1. Create the application object
IndustrySafetyCheckApp = Flask(__name__)
# CORS(IndustrySafetyCheckApp)


class ObjectDetectionClient:
    """Fetching Inputimage for PredictionPipeline"""
    def __init__(self):
        self.filename = "inputImage.jpg"


# 2. Routing to Home Page of "Industry Safety Check App"
#    (http://127.0.0.1:8080/)
@IndustrySafetyCheckApp.route("/", methods=["GET"])
@cross_origin()
def home():
    """This method renders the basic template for Flask App"""
    return render_template("index.html")

# 3. Routing to training status of "Industry Safety Check App"
#    (http://127.0.0.1:8080/)
@IndustrySafetyCheckApp.route("/train", methods=["GET", "POST"])
@cross_origin()
def train_route():
    """This method triggers training pipeline from Flask App"""
    obj = TrainingPipeline()
    obj.run_pipeline()
    return "Training done successfully!"


# 4. Routing to prediction result of "Industry Safety Check App"
#    (http://127.0.0.1:8080/)
@IndustrySafetyCheckApp.route("/predict", methods=['POST','GET'])
@cross_origin()
def predict_route():
    """This method triggers prediction pipeline from Flask App"""
    try:
        image = request.json['image']
        od_client = ObjectDetectionClient()
        decode_image(image, od_client.filename)

        os.system("cd yolov7/ && python detect.py --weights my_model.pt  --source ../data/inputImage.jpg")

        opencoded_base64 = encode_image_to_base64("yolov7/runs/detect/exp/inputImage.jpg")
        result = {"image": opencoded_base64.decode('utf-8')}
        # os.system("rm -rf yolov7/runs")

    except ValueError as val:
        print(val)
        return Response("Value not found inside  json data")
    except KeyError:
        return Response("Key value error incorrect key passed")
    except ODISCException as e:
        print(e)
        result = "Invalid input"

    return jsonify(result)


# 5. Run the API with gunicorn
#    Will run on http://127.0.0.1:8080
if __name__ == "__main__":
    IndustrySafetyCheckApp.run(host="0.0.0.0", port=8080,  debug=True)
    IndustrySafetyCheckApp.config["TEMPLATES_AUTO_RELOAD"] = True
