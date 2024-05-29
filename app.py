"""This is the main application module used for training or prediction using Flask API"""
from src.object_detection.pipeline.model_training_pipeline import TrainingPipeline

obj = TrainingPipeline()
obj.run_pipeline()
