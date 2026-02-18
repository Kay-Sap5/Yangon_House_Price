
from src.entity.artifact_entity.artifact import ModelTrainingArtifact
from src.constant.traning_pipeline import BEST_FINAL_MODEL_DIR , MODEL_TRAINING_FINAL_MODEL_FILE_NAME

from src.exception.exception import CustomException
from src.logging.logger import logging
from src.utils.utils import load_pkl_file
import sys
import os
import pandas as pd

class Prediction:
    def __init__(self):
        
        self.final_model_file_path   = os.path.join(
            BEST_FINAL_MODEL_DIR , MODEL_TRAINING_FINAL_MODEL_FILE_NAME
        )

    def initiate_prediction(self , data : pd.DataFrame) -> float:
        logging.info('Enterd inititate_prediction')
        self.ml_model = load_pkl_file(self.final_model_file_path)
        try:
            self.y_pred    = self.ml_model.predict(data)
            print(round(self.y_pred[0],2))
            return self.y_pred
        except Exception as e:
            raise CustomException(e,sys)
        

        

