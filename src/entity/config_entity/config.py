import os
import sys
from datetime import datetime
from src.constant import traning_pipeline
from src.logging.logger import logging
from src.exception.exception import CustomException

class TrainingPipelineConfig:
   
        def __init__(self,time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")):
            try:
                self.time : str = time
                self.training_pipeline = traning_pipeline
                self.artifact_name : str = self.training_pipeline.ARTIFACT_DIR_NAME
                self.artifact_dir : str = os.path.join(self.artifact_name , self.time)
            except Exception as e:
                raise CustomException(e,sys)
            

class DataIngestionConfig:
     def __init__(self , training_pipeline_config : TrainingPipelineConfig):
        try:
            self.training_pipeline_config = training_pipeline_config

            self.data_ingestion_dir = os.path.join(
                 self.training_pipeline_config.artifact_dir , traning_pipeline.DATA_INGESTION_DIR_NAME
            )

            self.data_ingestion_raw_dataset_file_path = os.path.join(
                 self.data_ingestion_dir , traning_pipeline.DATA_INGESTION_INGESED_DIR_NAME , traning_pipeline.DATA_INGESTION_DATASET_FILE_NAME
            )

            self.data_base_name = traning_pipeline.DATABASE_NAME
            self.collection_name = traning_pipeline.COLLECTION_NAME
            
        except Exception as e:
             raise CustomException(e,sys)
        
class DataPreproceessingConfig:
     def __init__(self,traning_pipeline_config : TrainingPipelineConfig):
          try:
               self.traning_pipeline_config = traning_pipeline_config

               self.data_preprocessing_dir = os.path.join(
                    self.traning_pipeline_config.artifact_dir , traning_pipeline.DATA_PREPROCESSING_DIR_NAME
               )
               
               self.data_preprocessing_full_data_dir = os.path.join(
                    self.data_preprocessing_dir , traning_pipeline.DATA_PREPROCESSING_fULL_DATA_DIR_NAME
               )
               self.data_preprocessing_full_data_file_path = os.path.join(
                    self.data_preprocessing_full_data_dir , traning_pipeline.DATA_PREPROCESSING_fULL_DATA_NAME
               )
               self.data_preprocessing_train_and_test_dir = os.path.join(
                    self.data_preprocessing_dir , traning_pipeline.DATA_PREPROCESSING_TRAIN_AND_TEST_DIR_NAME
               )

               self.data_preprocessing_train_file_path = os.path.join(
                    self.data_preprocessing_train_and_test_dir , traning_pipeline.TRAIN_DATA_NAME
               )

               self.data_preprocessing_test_file_path = os.path.join(
                    self.data_preprocessing_train_and_test_dir , traning_pipeline.TEST_DATA_NAME
               )
          except Exception as e:
               raise CustomException(e,sys)
          
class DataValidationConfig:
     def __init__(self , training_pipeline_config : TrainingPipelineConfig):
          try:
               self.training_pipeline_config = training_pipeline_config

               self.data_validation_dir = os.path.join(
                    self.training_pipeline_config.artifact_dir , traning_pipeline.DATA_VALIDATION_DIR_NAME
               )

               self.data_validation_valid_dir = os.path.join(
                    self.data_validation_dir , traning_pipeline.DATA_VALIDATION_VALID_DIR_NAME
               )

               self.data_validation_invalid_dir = os.path.join(
                    self.data_validation_dir , traning_pipeline.DATA_VALIDATION_INVALID_DIR_NAME
               )

               self.data_validation_valid_train_file_path = os.path.join(
                    self.data_validation_valid_dir , traning_pipeline.TRAIN_DATA_NAME
               )

               self.data_validation_valid_test_file_path = os.path.join(
                    self.data_validation_valid_dir , traning_pipeline.TEST_DATA_NAME
               )

               self.data_validation_invalid_train_file_path = os.path.join(
                    self.data_validation_invalid_dir , traning_pipeline.TRAIN_DATA_NAME
               )

               self.data_validation_invalid_test_file_path = os.path.join(
                    self.data_validation_invalid_dir , traning_pipeline.TEST_DATA_NAME
               )

               self.data_schema_file_path = traning_pipeline.DATA_SCHEMA_YAML_FILE_PATH
                    
          except Exception as e:
               raise CustomException(e,sys)
          
class DataFeatureEngineeringConfig:
     def __init__(self , training_pipeline_config : TrainingPipelineConfig):
          try:
               self.training_pipeline_config = training_pipeline_config

               self.feature_engineering_dir = os.path.join(
                    self.training_pipeline_config.artifact_dir , traning_pipeline.FEATURE_ENGINEERING_DIR_NAME
               )

               self.feature_engineering_applied_dir = os.path.join(
                    self.feature_engineering_dir , traning_pipeline.FEATURE_ENGINEERING_APPLIED_DATA_DIR
               )

               self.feature_engineering_train_file_path = os.path.join(
                    self.feature_engineering_applied_dir , traning_pipeline.TRAIN_DATA_NAME
               )

               self.feature_engineering_test_file_path = os.path.join(
                    self.feature_engineering_applied_dir , traning_pipeline.TEST_DATA_NAME
               )

               self.feature_engineering_data_feature_report_file_path = os.path.join(
                    self.feature_engineering_dir,traning_pipeline.FEATURE_ENGINEERING_DATA_FEATURE_REPORT_DIR,
                    traning_pipeline.FEATURE_ENGINEERING_DATA_FEATURE_REPORT_FILE_PATH
               )

          except Exception as e:
               raise CustomException(e,sys)

class DataTransformationConfig:
     def __init__(self , training_pipeline_config : TrainingPipelineConfig):
          try:
               self.training_pipeline_config = training_pipeline_config
               self.data_transformation_dir = os.path.join(
                    self.training_pipeline_config.artifact_dir,traning_pipeline.DATA_TRANSFORMATION_DIR_NAME
               )

               self.data_transformation_transformed_data_dir = os.path.join(
                    self.data_transformation_dir , traning_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR
               )

               self.data_transformation_transformed_train_file_path = os.path.join(
                    self.data_transformation_transformed_data_dir , traning_pipeline.TRAIN_DATA_NAME.replace('csv','npy')
               )

               self.data_transformation_transformed_test_file_path = os.path.join(
                    self.data_transformation_transformed_data_dir , traning_pipeline.TEST_DATA_NAME.replace("csv",'npy')
               )

               self.data_transformation_preprocessor_file_path = os.path.join(
                    self.data_transformation_dir , traning_pipeline.DATA_TRANSFORMATION_PREPROCESSOR_DIR_NAME , 
                    traning_pipeline.DATA_TRANSFORMATION_PREPROCESSOR_FILE_NAME
               )


          except Exception as e:
               raise CustomException(e,sys)

class ModelTrainingConfig:
     def __init__(self,training_pipeline_config : TrainingPipelineConfig):
          try:
               self.training_pipeline_config = training_pipeline_config

               self.model_training_dir_name = os.path.join(
                    self.training_pipeline_config.artifact_dir , traning_pipeline.MODEL_TRAINING_DIR_NAME)
               
               self.model_training_trained_model_dir = os.path.join(
                    self.model_training_dir_name , traning_pipeline.MODEL_TRAINING_TRAINED_MODEL_DIR_NAME
               )

               self.model_training_trained_model_file_path = os.path.join(
                    self.model_training_trained_model_dir , traning_pipeline.MODEL_TRAINING_TRAINED_MODEL_FILE_NAME
               )

               self.model_training_preprocessor_dir = os.path.join(
                    self.model_training_dir_name , traning_pipeline.MODEL_TRAINING_PREPROCESSOR_DIR_NAME
               )

               self.model_training_preprocessor_file_path = os.path.join(
                    self.model_training_preprocessor_dir , traning_pipeline.MODEL_TRAINING_TRAINED_MODEL_FILE_NAME
               )

               self.model_training_final_model_dir = os.path.join(
                    self.model_training_dir_name , traning_pipeline.MODEL_TRAINING_FINAL_MODEL_DIR
               )

               self.model_training_final_model_file_path = os.path.join(
                    self.model_training_final_model_dir , traning_pipeline.MODEL_TRAINING_FINAL_MODEL_FILE_NAME
               )
          except Exception as e:
               raise CustomException(e,sys)
