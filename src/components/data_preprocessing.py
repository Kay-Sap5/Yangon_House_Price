import os
import sys
import pandas as pd
import numpy as np

from src.exception.exception import CustomException
from src.logging.logger import logging
from src.entity.artifact_entity.artifact import DataPreprocessingArtifact , DataIngestionArtifact
from src.constant import traning_pipeline
from src.entity.config_entity.config import DataPreproceessingConfig
from src.extra_file.floor_trans import floor_trans
from sklearn.model_selection import train_test_split

class DataPreprocessing:
    def __init__(self, data_ingestion_artifact : DataIngestionArtifact,
                        data_preprocessing_config : DataPreproceessingConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_preprocessing_config = data_preprocessing_config
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod 
    def floor_str_to_int(x):
        key = list(floor_trans.keys())
        value = list(floor_trans.values())
        try:
            if x in key:
                ind = key.index(x)
                floor = value[ind]
                return float(np.round(floor,1))
            elif float(x):
                return x
        except:
            pass
        
        x = str(x).strip()
        if x ==str(np.nan) or x =="":
            return float(np.nan)
        

    @staticmethod
    def end_to_end_processing(dataframe : pd.DataFrame) -> pd.DataFrame:
        logging.info("Entering end_to_end_processing ............................................#####")
        try:
            df = dataframe
            # Step 1
            logging.info("Step 1")
            df = df.drop_duplicates()
            df.reset_index(inplace=True , drop=True)
            logging.info(f"Dropped Duplicate , shape {df.shape}")
            logging.info("Step 1 , Completed")

            # Step 2
            logging.info("Step 2")
            df.drop(columns = ['title','undertitle','date','propertydetail'],inplace = True)
            logging.info(f"Columns Left{df.columns}")
            logging.info("Step 2 , Completed")

            # Step 3 
            # Cleaning Price Column
            logging.info("Step 3")
            df['price'] = df['price'].str.replace(r"[^0-9.]",'',regex = True)
            df['price'] = df['price'].apply(lambda x:x if len(str(x))!= 0 else np.nan).astype(float)
            logging.info("Step 3 , Completed")

            # Step4
            # Extracting address
            logging.info("Step 4")
            df['state'] = df['address'].str.split(",").str[-1].str.strip().str.lower()
            df['city'] = df['address'].str.split(",").str[0].str.strip().str.lower()
            df = df[df['state'] =='yangon']
            df.reset_index(drop = True , inplace = True)
            df.drop(columns = ['address'] , inplace = True)
            logging.info(f"New Shape => {df.shape}")
            logging.info("Step 4 , Completed")
            

            # Step 5
            # Converting key_value_to_DataFrame
            logging.info("Step 5")
            df['key_value'] = df['key_value'].str.replace("[","").str.replace("]","")
            data = []

            for i in df['key_value'].str.split("),",regex = False):
                key = []
                value =[]
                for j in i:
                    k = j.split(",")[0].replace("('",'').replace("'",'').strip()
                    val = j.split(",")[1].replace("'",'').replace('"','').strip()
                    key.append(k)
                    value.append(val)
                data.append(dict(zip(key,value)))
            key_value_df = pd.DataFrame(data)
            key_value_df.reset_index(inplace = True , drop = True)
            logging.info(f"Key Value Dataframe  Created , Shape = {key_value_df.shape}")
            logging.info("Step 5 Completed")

            # Step 6
            # Select columns from key_value_df ['Type','Area','Bed Room','Bath Room','Floor']
            logging.info("Step 6")
            key_value_df = key_value_df[['Type','Area','Bed Room','Bath Room','Floor']]
            logging.info("Step 6 , Completed")

            # Step 7
            # Select Only ['Apartment','House','Condo'] from Type Variable
            logging.info("Step 7")
            key_value_df = key_value_df[key_value_df['Type'].isin(['Apartment','House','Condo'])]
            logging.info("Step 7 , Completed")

            # Step 8
            # Cleaning Area Column

            # Foot square_1 from foot square
            logging.info("Step 8")
            key_value_df['ft_square_1'] = key_value_df['Area'].apply(lambda x:x if 'ft<sup>2</sup>' in str(x) else str(0))
            key_value_df['ft_square_1'] = key_value_df['ft_square_1'].str.replace("ft<sup>2</sup>","").astype(float)
            logging.info("ft_square_1")

            # Foot square_2 from x_and_y
            key_value_df['area_x_y'] = key_value_df['Area'].apply(lambda x:x if 'x' in str(x) else str(0))
            x = key_value_df['area_x_y'].str.split("x").str[0].astype(float)
            y = key_value_df['area_x_y'].str.split("x").str[-1].astype(float)
            key_value_df['ft_square_2'] = x*y
            logging.info("ft_square_2")

            # Foot square_3 from acre
            # 1 acre = 43560 foot square
            key_value_df['acre'] = key_value_df['Area'].apply(lambda x :x if "acre" in str(x) else str(0))
            key_value_df['acre'] = key_value_df['acre'].str.replace("acre","").astype(float)
            key_value_df['ft_square_3'] = key_value_df['acre'] * 43560
            logging.info("ft_square_3")

            key_value_df["ft_square"] = key_value_df['ft_square_1'] + key_value_df['ft_square_2'] + key_value_df['ft_square_3'].isnull().sum() 
            logging.info("ft_square")

            key_value_df.drop(columns = ['Area','area_x_y','acre','ft_square_1','ft_square_2','ft_square_3'] , inplace = True)
            logging.info("Dropped ['Area','area_x_y','acre','ft_square_1','ft_square_2','ft_square_3']")
            # removing the the row where ft_square is zero
            key_value_df = key_value_df[key_value_df['ft_square'] != 0.0]
            logging.info(f"key_value_df {key_value_df.shape}")
            logging.info("Step 8 , Completed")

            # Step 9
            ## Cleaning Bed Room

            # converting the data type 
            logging.info("Step 9")
            key_value_df['Bath Room']=key_value_df['Bath Room'].astype(float)
            logging.info("Step 9 ,Completed")

            # Step 10
            # Converting the Bath Room data type
            logging.info("Step 10")
            key_value_df['Bath Room']=key_value_df['Bath Room'].astype(float)
            logging.info("Step 10 , Completed")

            # Step 11
            # Cleaning Floor
            logging.info("Step 11")
            key_value_df['Floor'] = key_value_df['Floor'].apply(DataPreprocessing.floor_str_to_int).astype(float)
            

            # Conacat two dataframe
            logging.info("Concatinating 2 DataFrames")
            result = pd.concat([df , key_value_df] , axis = 1)
            logging.info(f"Got New DataFrame , shape = {result.shape}")
            logging.info(f"Result columns : {result.columns}")
            logging.info("Step 11 , Completed")

            # Step 12
            # Delete key_value and apply dropna on the whole dataset
            logging.info("Step 12")
            result.drop(columns = ['key_value','state'] , inplace = True)
            result.dropna(inplace = True)
            logging.info(f'Drop na Done , new result shape  = {result.shape}')

            logging.info("Finishing end_to_end_processing  Successfully............................................#####")
            return result

        except Exception as e:
            raise CustomException(e,sys)

        
    def initiate_data_preprocessing(self):
        logging.info("Entered Data Preprocessing")
        try:
            
            self.df = pd.read_csv(self.data_ingestion_artifact.raw_dataset_file_path)
            logging.info(f"DataFrame Loaded , shape {self.df.shape}")
            self.result = DataPreprocessing.end_to_end_processing(self.df)

            os.makedirs(os.path.dirname(self.data_preprocessing_config.data_preprocessing_full_data_file_path),exist_ok=True)

            self.result.to_csv(self.data_preprocessing_config.data_preprocessing_full_data_file_path , index=False , header = True)
            logging.info("full data saved")
            train_set , test_set = train_test_split(self.result, test_size=traning_pipeline.TRAIN_TEST_SPLIT_RATIO)

            os.makedirs(os.path.dirname(self.data_preprocessing_config.data_preprocessing_train_file_path),exist_ok=True)

            train_set.to_csv(self.data_preprocessing_config.data_preprocessing_train_file_path , index = False ,header = True )
            test_set.to_csv(self.data_preprocessing_config.data_preprocessing_test_file_path , index = False , header = True)
            logging.info("train and test data saved")
            data_preprocessing_artifact = DataPreprocessingArtifact(train_data_file_path=self.data_preprocessing_config.data_preprocessing_train_file_path,
                                      test_data_file_path=self.data_preprocessing_config.data_preprocessing_test_file_path)
            
            return data_preprocessing_artifact

        except Exception as e:
            raise CustomException(e,sys)