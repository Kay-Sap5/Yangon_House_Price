import requests
from src.exception.exception import CustomException
from src.logging.logger import logging
from src.constant.traning_pipeline import LINK_SCRAPPER_SAVED_LINK_FILE_PATH
from src.update_database.scraper_artifact.scraper_artifact import ScrapeNewLinkArtifact
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
import sys



class ScrapeNewLink:
    def __init__(self):
        self.num_of_pages :int = 20
        self.links_file_path :str= LINK_SCRAPPER_SAVED_LINK_FILE_PATH
        self.headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'DNT': '1',  # Do Not Track
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1'
                    }
    def filter_new_link(self, new_dataframe : pd.DataFrame) -> np.array:
        logging.info("Entered Fileter_new_link method")
        try:
            self.base_dataframe = pd.read_csv(LINK_SCRAPPER_SAVED_LINK_FILE_PATH)
            logging.info("base dataframe Loaded....")
            self.new_dataframe = new_dataframe

            self.filtered_dataframe = self.new_dataframe[~self.new_dataframe['Links'].isin(self.base_dataframe['Links'])]
            if self.filtered_dataframe.shape[0] == 0:
                logging.info(f"filterd DataFrame Shape {self.filtered_dataframe.shape}")
                quit()
            logging.info("filtered data frame successfully")
            return self.filtered_dataframe.values.flatten()
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_scrape_new_link(self):
        logging.info("Entered initiate_scrape_new_link method")
        try:
            links = []
            for i in range(self.num_of_pages):
                url = f"https://shweproperty.com/en/property/search/for-sale/all/all/all/min-max?&page={i}"
                self.stoped_file_path = f'Stopped_Data/till{i}.csv'
                main_page = requests.get(url , headers=self.headers).text
                main_page_soup = BeautifulSoup(main_page , 'html.parser')

                container = main_page_soup.find(class_ = 'twelve wide column')
                blocks  = container.find_all(class_ = "serp__block")

                for j in blocks:
                    links.append(j.find('a').get('href'))

                logging.info(f"Complete Pages --> {i}")

            logging.info(f"Total Links {len(links)}")

            new_df = pd.DataFrame({"Links":links})
            os.makedirs(os.path.dirname(self.links_file_path),exist_ok=True)
            
            logging.info(f"Links DataFrame shape =>  {new_df.shape}")

            self.filtered_link_arr = self.filter_new_link(new_dataframe=new_df)
            scrape_new_link_artifact = ScrapeNewLinkArtifact(self.filtered_link_arr)

            return scrape_new_link_artifact

        except Exception as e:
            raise CustomException(e,sys)


if __name__ == "__main__":
    obj = ScrapeNewLink()
    scrape_new_link_artifact = obj.initiate_scrape_new_link()
    print(scrape_new_link_artifact.new_links.shape)


