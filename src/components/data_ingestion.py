import os
import sys
import pymongo
from dotenv import load_dotenv
import pandas as pd
from src.logging.logger import logging
from src.exception.exception import CustomException

from src.entity.config_entity.config import (DataIngestionConfig , DataPreproceessingConfig ,
                                    TrainingPipelineConfig , DataValidationConfig,
                                    DataFeatureEngineeringConfig,DataTransformationConfig ,
                                    ModelTrainingConfig)
from src.entity.artifact_entity.artifact import DataIngestionArtifact 

from src.components.data_preprocessing import DataPreprocessing
from src.components.data_validation import DataValidation
from src.components.data_feature_engineering import DataFeatureEngineering
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTraining

class DataIngestion:
    def __init__(self , data_ingestion_config : DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_collection_data(self):
        try:
            logging.info("Entered_get_collection_data")
            load_dotenv()
            MONGO_DB_URL = os.getenv('MONGO_DB_URL')
            self.client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.client[self.data_ingestion_config.data_base_name]
            self.collection = self.database[self.data_ingestion_config.collection_name]
            self.data = self.collection.find()
            
            logging.info("extract data successfully")
            return self.data
        except Exception as e:
            raise CustomException(e,sys)
  
        
    def initiate_data_ingestion(self):
        logging.info("Entered initiate_data_ingestion")
        try:
            os.makedirs(os.path.dirname(self.data_ingestion_config.data_ingestion_raw_dataset_file_path) , exist_ok=True)
            self.data = list(self.get_collection_data())
            
            df = pd.DataFrame(self.data)
            logging.info(f"DataFrame Created , file shape = ({df.shape})")
            if '_id' in df.columns:
                df.drop(columns=['_id'],inplace =True)
                logging.info(f"Deleting the (_id) column from the dataframe")
            df.to_csv(self.data_ingestion_config.data_ingestion_raw_dataset_file_path , index=False , header = True)
            logging.info("DataFrame Saved")
            return DataIngestionArtifact(self.data_ingestion_config.data_ingestion_raw_dataset_file_path)
        
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    training_pipeline_config  = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig()
    obj = DataIngestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = obj.initiate_data_ingestion()
    
    data_preporcessing_config = DataPreproceessingConfig(training_pipeline_config)
    data_preprocessing = DataPreprocessing(data_ingestion_artifact=data_ingestion_artifact,
                      data_preprocessing_config=data_preporcessing_config)
    data_preprocessing_artifact = data_preprocessing.initiate_data_preprocessing()
    
    data_validation_config  = DataValidationConfig(training_pipeline_config)
    data_validation = DataValidation(data_validation_config=data_validation_config,
                   data_preprocessing_artifact=data_preprocessing_artifact)
    
    data_validation_artifact = data_validation.initiate_data_validation()
    
    data_feature_engineering_config = DataFeatureEngineeringConfig(training_pipeline_config)
    data_feature_engineering = DataFeatureEngineering(data_validation_artifact=data_validation_artifact,
                                                      data_feature_engineering_config=data_feature_engineering_config)
    
    data_feature_engineering_artifact = data_feature_engineering.initiate_data_feature_engineering()
    
    data_transformation_config = DataTransformationConfig(training_pipeline_config)
    data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                             data_feature_engineering_artifact=data_feature_engineering_artifact)
    
    data_transformation_artifact = data_transformation.initiate_data_transformation()
    
    model_training_config = ModelTrainingConfig(training_pipeline_config=training_pipeline_config)
    model_training = ModelTraining(model_training_config=model_training_config , 
                                   data_transformation_artifact=data_transformation_artifact)
    
    model_training_artifact = model_training.initiate_model_training()
    print(model_training_artifact)
