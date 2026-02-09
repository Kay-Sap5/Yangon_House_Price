import os
import sys
import numpy as np

from src.exception.exception import CustomException
from src.logging.logger import logging

from src.entity.config_entity.config import ModelTrainingConfig
from src.entity.artifact_entity.artifact import DataTransformationArtifact , ModelTrainingArtifact
from src.components.model_evaluation import ModelEvaluationMetic

from src.utils.utils import load_pkl_file , load_npy_file , save_pkl_file
from src.utils.ml_ultis import models , param_grids , model_trainer , NetworkModel

class ModelTraining:
    def __init__(self,model_training_config :ModelTrainingConfig,
                        data_transformation_artifact : DataTransformationArtifact):
        try:
            self.model_training_config = model_training_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def find_best_model(self , model_score : dict):
        logging.info('Entered final_best_model method')
        try:
            self.model_score = model_score
            name = list(model_score.keys())
            score = list(model_score.values())

            best_score = max(score)
            best_model_name = name[score.index(best_score)]
            logging.info(f"Model = {best_model_name} , R2_Score =  {best_score}")
            return best_model_name , best_score
        except Exception as e:
            raise CustomException(e,sys) 

    def initiate_model_training(self):
        logging.info('Entered initiate_model_training.......')
        try:
            self.train_arr_file_path = self.data_transformation_artifact.transformed_train_data_file_path
            self.test_arr_file_path  = self.data_transformation_artifact.transformed_test_data_file_path
            print(self.train_arr_file_path)

            self.train_arr = load_npy_file(self.train_arr_file_path)
            self.test_arr  = load_npy_file(self.test_arr_file_path)
            
            logging.info('Train and Test Array Loaded...')

            self.x_train = self.train_arr[:,:-1]
            self.y_train = self.train_arr[:,-1]

            self.x_test  = self.test_arr[:,:-1]
            self.y_test  = self.test_arr[:,-1]

            self.preprocessor = load_pkl_file(self.data_transformation_artifact.transformed_preprocessor_file_path,)
            logging.info('Preprocessor File Loaded...')


            self.models_score = model_trainer(
                x_train=self.x_train,
                x_test=self.x_test,
                y_train=self.y_train,
                y_test=self.y_test,
                models=models,
                params=param_grids)
            
            self.best_model_name , self.best_score = self.find_best_model(model_score=self.models_score)

            self.best_model = models[self.best_model_name]

            print(self.best_model , self.best_score)

            self.network_model = NetworkModel(
                preprocessor=self.preprocessor,
                model=self.best_model)
            
            save_pkl_file(self.model_training_config.model_training_final_model_file_path , self.network_model)

            y_train_pred = self.best_model.predict(self.x_train)
            y_test_pred  = self.best_model.predict(self.x_test)

            train_eval_metric_obj = ModelEvaluationMetic(y_true=self.y_train , y_pred=y_train_pred)
            train_eval_metric = train_eval_metric_obj.initiate_model_evaluation_metric()

            test_eval_metric_obj  = ModelEvaluationMetic(y_true=self.y_test , y_pred=y_test_pred)
            test_eval_metric = test_eval_metric_obj.initiate_model_evaluation_metric()

            logging.info(f"Train Shape = {np.shape(self.x_train)} , Test Shape = {np.shape(self.x_test)}")
            self.model_trainer_artifact = ModelTrainingArtifact(
                trained_final_model_file_path=self.model_training_config.model_training_final_model_file_path,
                train_model_evaluation=train_eval_metric,
                test_model_evaluation=test_eval_metric)
            logging.info(f"Train Evaluation Metric {train_eval_metric}" )
            logging.info(f"Test Evaluation Metric {test_eval_metric}")
            return self.model_trainer_artifact

        except Exception as e:
            raise CustomException(e,sys)