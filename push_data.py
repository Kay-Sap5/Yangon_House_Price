from src.logging.logger import logging
from src.exception.exception import CustomException

import os
import sys
import pymongo
import certifi
import json
from dotenv import load_dotenv
import pandas as pd
import numpy as np

load_dotenv()
certifi.where()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class Upload_data_mongo:
    def __init__(self):
        pass

    def convert_csv_to_json(self,file_path):
        try:
            logging.info("Entered convert_csv_to_json")

            df = pd.read_csv(file_path,)
            df.reset_index(drop=True , inplace=True)
            records = list(json.loads(df.T.to_json()).values())

            logging.info("Converting Successful....")
            return records

        except Exception as e:
            raise CustomException(e,sys)
        
    def push_to_mongo(self , database_name , collection_name , records):

        self.database_name = database_name
        self.collection_name = collection_name

        try:
            logging.info("Entered connect_to_mongo")
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database  = self.mongo_client[self.database_name]
            self.collection = self.database[self.collection_name]

            self.collection.insert_many(records)
            logging.info("pushed_data_successfully")

        except Exception as e:
            raise CustomException(e,sys)
    

if __name__ == '__main__':

    database_name = 'House_Price_Shwe_Property'
    collection_name = 'raw_scraped_data'
    # csv_file_path = "C:\Users\M S I\Desktop\Myanmar_Houses_Price_Prediction\Scrapped_Data\dataset.csv"
    csv_file_path = r'Scrapped_Data\dataset.csv'

    obj = Upload_data_mongo()
    records = obj.convert_csv_to_json(file_path=csv_file_path)
    obj.push_to_mongo(database_name=database_name , collection_name=collection_name , records=records)

    
