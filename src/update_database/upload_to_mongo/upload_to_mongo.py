import os
import sys

from src.update_database.scraper_artifact.scraper_artifact import ScrapeDataArtifact
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.constant import LINK_SCRAPPER_SAVED_LINK_FILE_PATH

import pymongo
import certifi
from dotenv import load_dotenv
import pandas as pd
import json
from src.update_database.scraper_artifact.scraper_artifact import ScrapeNewLinkArtifact
from src.constant import DATABASE_NAME , COLLECTION_NAME

class UploadToMongo:
    def __init__(self,scrape_data_artifact : ScrapeDataArtifact,
                 scrape_new_link_artifact:ScrapeNewLinkArtifact):
        try:
            load_dotenv()
            self.MONGO_DB_URL = os.getenv("MONGO_DB_URL")
            self.database_name = DATABASE_NAME
            self.collection_name = COLLECTION_NAME
            self.new_link_arr = scrape_new_link_artifact.new_links
            self.scrape_data_artifact = scrape_data_artifact

        except Exception as e:
            raise CustomException(e,sys)
    
    def convert_df_to_json(self,dataframe : pd.DataFrame):
        try:
            logging.info("Entered convert_df_to_json")

            self.df = dataframe
            self.df.reset_index(drop=True , inplace=True)
            self.records = list(json.loads(self.df.T.to_json()).values())

            logging.info("Converting Successful....")
            return self.records
        except Exception as e:
            raise CustomException(e,sys)
        
    def add_new_links_to_base(self,arr):
        try:
            self.new_df = pd.DataFrame({"Links":arr})
            self.base_df = pd.read_csv(LINK_SCRAPPER_SAVED_LINK_FILE_PATH)
            logging.info(f"New Link Data Shape{self.new_df.shape}\n Base Data Shape{self.base_df.shape}")

            self.final_dataframe = pd.concat([self.new_df , self.base_df])
            self.final_dataframe.reset_index(drop=True)
            self.final_dataframe.to_csv(LINK_SCRAPPER_SAVED_LINK_FILE_PATH , index=False , header=True)
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_upload_to_mongo(self):
        logging.info(" Entered initiate_upload_to_mongo")
        try:
            self.dataframe = self.scrape_data_artifact.dataframe

            logging.info("Connecting To Mongo DB.....")
            self.client = pymongo.MongoClient(self.MONGO_DB_URL)
            self.database = self.client[self.database_name]
            self.collection = self.database[self.collection_name]
            logging.info("Connected To Mongo DB")
        
            self.records = self.convert_df_to_json(self.dataframe)
            logging.info("Successfully Converted DataFrame To Json")
            
            self.uploaded_status : bool = False
            try:
                self.collection.insert_many(self.records)
                logging.info("Uploaded Data to the Data Base Successfully...")
                self.uploaded_status = True
            finally:
                
                if self.uploaded_status:
                    self.add_new_links_to_base(self.new_link_arr)
                else:
                    logging.warning("Data Cannot Upload To The Mongo DB")
            
            logging.info(f"{len(self.records)}")
            print(len(self.records))
        except Exception as e:
            raise CustomException(e,sys)