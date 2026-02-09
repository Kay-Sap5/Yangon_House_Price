from sklearn.metrics import (mean_absolute_error , mean_absolute_percentage_error,
                             root_mean_squared_error , mean_squared_error,r2_score)
from src.logging.logger import logging
from src.exception.exception import CustomException
import sys
from src.entity.artifact_entity.artifact import ModelEvaluationMetricsArtifact

class ModelEvaluationMetic:
    def __init__(self , y_true , y_pred):
        try:
            self.y_true = y_true
            self.y_pred = y_pred
        except Exception as e:
            raise  CustomException(e,sys)
    def initiate_model_evaluation_metric(self):
        try:
            self.mse = mean_squared_error(y_true=self.y_true , y_pred=self.y_pred)
            self.mae = mean_absolute_error(y_true=self.y_true , y_pred=self.y_pred)
            self.rmse = root_mean_squared_error(y_true=self.y_true , y_pred=self.y_pred)
            self.mape = mean_absolute_percentage_error(y_true=self.y_true , y_pred=self.y_pred)
            self.r2   = r2_score(y_true=self.y_true , y_pred=self.y_pred)

            model_evaluation_metric_artifact = ModelEvaluationMetricsArtifact(
                r2_score=self.r2,
                mean_absolute_error=self.mae,
                mean_square_error=self.mse,
                root_mean_square_error=self.rmse,
                mean_absolute_percentage_error=self.mape
            )
            
            return model_evaluation_metric_artifact

        except Exception as e:
            raise CustomException(e,sys)