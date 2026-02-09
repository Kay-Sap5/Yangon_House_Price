import os
import sys
import numpy as np
import pandas as pd
from src.logging.logger import logging
from src.exception.exception import CustomException

from src.entity.artifact_entity.artifact import DataValidationArtifact , DataFeatureEngineeringArtifact
from src.entity.config_entity.config import DataFeatureEngineeringConfig


from src.utils.utils import feature_detail_dict , write_yaml_file
class DataFeatureEngineering:
    def __init__(self , data_validation_artifact : DataValidationArtifact ,
                        data_feature_engineering_config : DataFeatureEngineeringConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_feature_engineering_config = data_feature_engineering_config
        except Exception as e:
            raise CustomException(e,sys)
        

    def outlier_treatment(self,train : pd.DataFrame ,
                           test : pd.DataFrame ,
                             column : str):
        try:
            q1 = train[column].quantile(0.25)
            q3 = train[column].quantile(0.75)
            iqr = q3 - q1
            
            lower = q1 - (1.5 * iqr)
            upper = q3 + (1.5 * iqr)
            
            # Efficiently caps values below lower and above upper
            return train[column].clip(lower=lower, upper=upper) , test[column].clip(lower = lower , upper = upper)
        except Exception as e:
            raise CustomException(e,sys)
        
    def arrange_cat(self,train : pd.DataFrame ,
                        test : pd.DataFrame , 
                        column : str , threshold = 20 , replacing :str = "Others"):
        try:
            count = train[column].value_counts()
            rare_count = count[count<threshold].index
            return train[column].replace(rare_count , replacing) , test[column].replace(rare_count , replacing)
        except Exception as e:
            raise CustomException(e,sys)

    def arrange_floor(self , train : pd.DataFrame ,
                        test : pd.DataFrame , 
                        column : str , threshold = 6):
        try:
            train[column] = np.round(train[column],0)
            test[column] = np.round(test[column],0)
            return train[column].apply(lambda x:x if x<threshold else 7).astype(int), test[column].apply(lambda x:x if x<threshold else 7).astype(int)
        except Exception as e:
            raise CustomException(e,sys) 
        
    def initiate_data_feature_engineering(self):
        logging.info('Entered initiate_data_feature_engineering')
        try:
            self.train_data = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            self.test_data  = pd.read_csv(self.data_validation_artifact.valid_test_file_path) 
            logging.info("Train and Test Data Loaded.....")
            self.train_data['price'] , self.test_data['price'] =  self.outlier_treatment(train=self.train_data ,
                                                                                test=self.test_data ,
                                                                                  column='price')
            logging.info("Train and Test Price column Outlier Treated")

            self.train_data['ft_square'] , self.test_data['ft_square'] = self.outlier_treatment(train=self.train_data,
                                                                                test=self.test_data,
                                                                                column='ft_square')
            logging.info("Train and Test Ft_Square column Outlier Treated")

            self.train_data['city'] , self.test_data['city'] = self.arrange_cat(train=self.train_data,
                                                                      test=self.test_data,
                                                                      column='city',
                                                                      threshold=20)
            logging.info("Train and Test City Column arranged")

            self.train_data['Floor'] , self.test_data['Floor'] = self.arrange_floor(train=self.train_data,
                                                                      test=self.test_data,
                                                                      column='Floor',
                                                                      threshold=6)
           

            logging.info("Train and Test Floor Column arranged")

            feature_dict = feature_detail_dict(self.train_data , self.test_data)
            os.makedirs(os.path.dirname(self.data_feature_engineering_config.feature_engineering_data_feature_report_file_path),exist_ok=True)

            write_yaml_file(self.data_feature_engineering_config.feature_engineering_data_feature_report_file_path,feature_dict)
            
            os.makedirs(os.path.dirname(self.data_feature_engineering_config.feature_engineering_train_file_path),exist_ok=True)
            os.makedirs(os.path.dirname(self.data_feature_engineering_config.feature_engineering_test_file_path),exist_ok=True)

            self.train_data.to_csv(self.data_feature_engineering_config.feature_engineering_train_file_path)
            self.test_data.to_csv(self.data_feature_engineering_config.feature_engineering_test_file_path)

            data_feature_engineering_artifact = DataFeatureEngineeringArtifact(
                    feature_engineering_train_file_path=self.data_feature_engineering_config.feature_engineering_train_file_path,
                    feature_engineering_test_file_path=self.data_feature_engineering_config.feature_engineering_test_file_path
            )

            return data_feature_engineering_artifact


        except Exception as e:
            raise CustomException(e,sys)