import os
import sys
import pandas as pd
import numpy as np

from src.logging.logger import logging
from src.exception.exception import CustomException

from src.entity.config_entity.config import DataTransformationConfig
from src.entity.artifact_entity.artifact import DataFeatureEngineeringArtifact , DataTransformationArtifact

from sklearn.preprocessing import OneHotEncoder , MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from src.constant import traning_pipeline
from src.utils.utils import save_arr_to_npy , save_pkl_file

class DataTransformation:
    def __init__(self , data_transformation_config : DataTransformationConfig , 
                        data_feature_engineering_artifact : DataFeatureEngineeringArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_feature_engineering_artifact = data_feature_engineering_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def preporcessor(self,num_feature , cat_feature):
        try:
            self.num_features = num_feature
            self.cat_features = cat_feature

            num_pipeline = Pipeline(steps=[
                ('SimpleImputer',SimpleImputer(strategy='median')),
                ("MinMaxScaler",MinMaxScaler())
            ])

            cat_pipeline = Pipeline(steps=[
                ("SimpleImputer",SimpleImputer(strategy="most_frequent")),
                ('OneHotEncoder',OneHotEncoder(handle_unknown='ignore'))
            ])

            transformer = ColumnTransformer([
                ('num_pipeline',num_pipeline,self.num_features),
                ('cat_pipeline',cat_pipeline , self.cat_features)
            ])

            return transformer

        except Exception as e:
            raise CustomException(e,sys)
    def initiate_data_transformation(self):
        try:
            train_data = pd.read_csv(self.data_feature_engineering_artifact.feature_engineering_train_file_path)
            test_data  = pd.read_csv(self.data_feature_engineering_artifact.feature_engineering_test_file_path)
            TARGET_NAME = traning_pipeline.TARGET_NAME

            train_feature = train_data.drop(columns = TARGET_NAME)
            train_target  = train_data[TARGET_NAME]

            test_feature = test_data.drop(columns = TARGET_NAME)
            test_target  = test_data[TARGET_NAME]

            self.num_feature = train_feature.select_dtypes(exclude='O').columns
            self.cat_feature = train_feature.select_dtypes(include='O').columns

            self.preporcessor_file = self.preporcessor(num_feature=self.num_feature , cat_feature=self.cat_feature)
            self.preporcessor_file.fit(train_feature)

            save_pkl_file(self.data_transformation_config.data_transformation_preprocessor_file_path , self.preporcessor_file)

            transformed_train_data = self.preporcessor_file.transform(train_feature).toarray()
            transformed_test_data = self.preporcessor_file.transform(test_feature).toarray()
            logging.warning(f"Transformed Train Data shape = {np.shape(transformed_train_data)} , Transformed Test Data Shape = {np.shape(transformed_test_data)}")
            logging.info(f"Train Feature {np.shape(train_feature)} , Target {train_target.shape}")
            
            full_transformed_train = np.c_[transformed_train_data , np.array(train_target)]
            full_transformed_test = np.c_[transformed_test_data , np.array(test_target)]
            

            save_arr_to_npy(self.data_transformation_config.data_transformation_transformed_train_file_path,
                             full_transformed_train)
            save_arr_to_npy(self.data_transformation_config.data_transformation_transformed_test_file_path,
                             full_transformed_test)
            
            data_transformation_artifact = DataTransformationArtifact(transformed_train_data_file_path=self.data_transformation_config.data_transformation_transformed_train_file_path,
                                        transformed_test_data_file_path=self.data_transformation_config.data_transformation_transformed_test_file_path,
                                        transformed_preprocessor_file_path=self.data_transformation_config.data_transformation_preprocessor_file_path)
            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e,sys)