from src.update_database.Scraper.new_link_scrapper import ScrapeNewLink
from src.update_database.Scraper.scrape_data import ScrapData
from src.update_database.scraper_artifact.scraper_artifact import ScrapeDataArtifact
from src.update_database.upload_to_mongo.upload_to_mongo import UploadToMongo

import os
import sys

from src.logging.logger import logging
from src.exception.exception import CustomException

if __name__ == "__main__":
    obj = ScrapeNewLink()
    scrape_new_link_artifact = obj.initiate_scrape_new_link()

    scrape_data_obj = ScrapData(srcape_new_link_artifact=scrape_new_link_artifact)
    scrape_data_artifact = scrape_data_obj.initiate_scrap_data()
    
    upload_to_mongo = UploadToMongo(scrape_data_artifact=scrape_data_artifact , 
                                    scrape_new_link_artifact=scrape_new_link_artifact)
    upload_to_mongo.initiate_upload_to_mongo()



