import os
import sys

from src.logging.logger import logging
from src.exception.exception import CustomException

from src.components.data_ingestion import DataIngestion
from src.components.data_preprocessing import DataPreprocessing
from src.components.data_validation import DataValidation
from src.components.data_feature_engineering import DataFeatureEngineering
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTraining

from src.entity.config_entity.config import (
    DataIngestionConfig,
    DataPreproceessingConfig,
    DataValidationConfig,
    DataFeatureEngineeringConfig,
    DataTransformationConfig,
    ModelTrainingConfig,
    TrainingPipelineConfig)

from src.entity.artifact_entity.artifact import (
    DataIngestionArtifact,
    DataPreprocessingArtifact,
    DataValidationArtifact,
    DataFeatureEngineeringArtifact,
    DataTransformationArtifact,
    ModelTrainingArtifact
)

class TrainingPipeline:
    def __init__(self):
        try:
            self.training_pipline_config = TrainingPipelineConfig()
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_ingestion(self):
        logging.info('Training PipleLine (start_data_ingestion)')
        try:
            self.data_ingestion_config = DataIngestionConfig(self.training_pipline_config)
            self.data_ingestion = DataIngestion(self.data_ingestion_config)
            self.data_ingestion_artifact = self.data_ingestion.initiate_data_ingestion()

            return self.data_ingestion_artifact

        except Exception as e:
            raise CustomException(e,sys)
    
    def start_data_preprocessing(self , data_ingestion_artifact : DataIngestionArtifact):
        logging.info('Training PipleLine (start_data_preprocessing)')
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_preprocessing_config = DataPreproceessingConfig(self.training_pipline_config)
            self.data_preprocessing = DataPreprocessing(data_ingestion_artifact=self.data_ingestion_artifact,
                                                        data_preprocessing_config=self.data_preprocessing_config)

            self.data_preprocessing_artifact = self.data_preprocessing.initiate_data_preprocessing()

            return self.data_preprocessing_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_validation(self , data_preprocessing_artifact : DataPreprocessingArtifact):
        logging.info('Training PipleLine (start_data_validation)')
        try:
            self.data_preprocessing_artifact = data_preprocessing_artifact
            self.data_validation_config = DataValidationConfig(self.training_pipline_config)

            self.data_validation = DataValidation(data_validation_config=self.data_validation_config,
                                                  data_preprocessing_artifact=self.data_preprocessing_artifact)
            self.data_validation_artifact = self.data_validation.initiate_data_validation()

            return self.data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_feature_engineering(self , data_validation_artifact : DataValidationArtifact):
        logging.info('Training PipleLine (start_data_feature_engineering)')
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_feature_engineering_config = DataFeatureEngineeringConfig(self.training_pipline_config)
            self.data_feature_engineering = DataFeatureEngineering(data_feature_engineering_config=self.data_feature_engineering_config,
                                                                   data_validation_artifact=self.data_validation_artifact)

            self.data_feature_engineering_artifact = self.data_feature_engineering.initiate_data_feature_engineering()
            return self.data_feature_engineering_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_transformation(self , data_feature_engineeing_artifact : DataFeatureEngineeringArtifact):
        logging.info('Training PipleLine (start_data_transformation)')
        try:
            self.data_validation_artifact = data_feature_engineeing_artifact
            self.data_transformation_config = DataTransformationConfig(self.training_pipline_config)
            self.data_transformation = DataTransformation(data_feature_engineering_artifact=self.data_feature_engineering_artifact,
                                                          data_transformation_config=self.data_transformation_config)
            self.data_transformation_artifact = self.data_transformation.initiate_data_transformation()
            return self.data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_model_trainer(self , data_transformation_artifact : DataTransformationArtifact):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = ModelTrainingConfig(self.training_pipline_config)
            self.model_trainer = ModelTraining(data_transformation_artifact=self.data_transformation_artifact,
                                               model_training_config=self.model_trainer_config)
            self.model_trainer_artifact = self.model_trainer.initiate_model_training()
            return self.model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_preprocessing_artifact = self.start_data_preprocessing(data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact = self.start_data_validation(data_preprocessing_artifact=data_preprocessing_artifact)
            data_feature_engineering_artifact = self.start_data_feature_engineering(data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = self.start_data_transformation(data_feature_engineeing_artifact=data_feature_engineering_artifact)

            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e,sys)


if __name__ == '__main__':
    training_pipeline = TrainingPipeline()
    training_pipeline.run_pipeline()
