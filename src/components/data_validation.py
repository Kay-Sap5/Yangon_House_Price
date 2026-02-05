import os
import sys
import pandas as pd

from src.logging.logger import logging
from src.exception.exception import CustomException

from src.entity.config_entity.config import DataValidationConfig
from src.entity.artifact_entity.artifact import DataValidationArtifact , DataPreprocessingArtifact
from src.utils.utils import load_yaml_file


class DataValidation:
    def __init__(self , data_validation_config : DataValidationConfig,
                        data_preprocessing_artifact : DataPreprocessingArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_preprocessing_artifact = data_preprocessing_artifact

        except Exception as e:
            raise CustomException(e,sys)
        
    def validate_data_columns(self,train_data : pd.DataFrame , test_data : pd.DataFrame):
        logging.info("Entered validate_data_columns")
        try:
            schema = load_yaml_file(self.data_validation_config.data_schema_file_path)
            schema_full_columns = schema['full_columns']
            schema_full_columns.sort()

            schema_cat_columns  = schema['cat_columns']
            schema_cat_columns.sort()

            schema_num_columns  = schema['num_columns']
            schema_num_columns.sort()

            # Train Data
            train_full_columns = list(train_data.columns)
            train_full_columns.sort()

            train_cat_columns = list(train_data.select_dtypes('O'))
            train_cat_columns.sort()

            train_num_columns = list(train_data.select_dtypes(exclude='O'))
            train_num_columns.sort()

            # Test Data
            test_full_columns = list(test_data.columns)
            test_full_columns.sort()

            test_cat_columns = list(test_data.select_dtypes('O'))
            test_cat_columns.sort()

            test_num_columns = list(test_data.select_dtypes(exclude='O'))
            test_num_columns.sort()

            status = False
            if schema_full_columns == train_full_columns == test_full_columns:
                logging.info("Full Columns matches Successfully")
                if schema_num_columns == train_num_columns == test_num_columns:
                    logging.info("Numerical Columns matches Successfully")
                    if schema_cat_columns == train_cat_columns == test_cat_columns:
                        logging.info("Categorical Columns matches Successfully")
                        logging.info("Data Columns Validated Successfully.......")
                        status=True
                        
                    
                    else:
                        logging.info("Categoical Columns Not matches")
                else:
                    logging.info("Numerical Columns Not Matches")
            else:
                logging.info("Full Columns Not matches")
            return status
                

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_validation(self):
        try:
            train_df = pd.read_csv(self.data_preprocessing_artifact.train_data_file_path)
            test_df  = pd.read_csv(self.data_preprocessing_artifact.test_data_file_path)

            status = self.validate_data_columns(train_data=train_df , test_data= test_df)
            if status:
                os.makedirs(os.path.dirname(self.data_validation_config.data_validation_valid_train_file_path) , exist_ok=True)

                train_df.to_csv(self.data_validation_config.data_validation_valid_train_file_path , index=False , header = True)
                test_df.to_csv(self.data_validation_config.data_validation_valid_test_file_path , index=False , header = True)
                logging.info("Valid Data Saved ")
                
                data_validation_artifact = DataValidationArtifact(valid_train_file_path=self.data_validation_config.data_validation_valid_train_file_path ,
                                       valid_test_file_path=self.data_validation_config.data_validation_valid_test_file_path)
                return data_validation_artifact
            else:
                os.makedirs(os.path.dirname(self.data_validation_config.data_validation_invalid_train_file_path) , exist_ok=True)

                train_df.to_csv(self.data_validation_config.data_validation_invalid_train_file_path , index=False , header = True)
                test_df.to_csv(self.data_validation_config.data_validation_invalid_test_file_path , index=False , header = True)
                logging.warning("Invalid Data Saved!!!!!!!")

                data_validation_artifact = DataValidationArtifact(valid_train_file_path=None ,
                                       valid_test_file_path=None)
                return data_validation_artifact

            

        except Exception as e:
            raise CustomException(e,sys)
        
