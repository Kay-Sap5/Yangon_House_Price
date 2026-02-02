import requests
from src.exception.exception import CustomException
from src.logging.logger import logging
from src.constant import LINK_SCRAPPER_SAVED_LINK_FILE_PATH
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys



class Scrape_Link:
    def __init__(self):
        self.num_of_pages :int = 539
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
        
    def initiate_scrape_link(self):
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

            df = pd.DataFrame({"Links":links})
            os.makedirs(os.path.dirname(self.links_file_path),exist_ok=True)

            logging.info(f"Links DataFrame shape =>  {df.shape}")

            df.to_csv(self.links_file_path , index=False , header=True)
            logging.info("Links DataFrame Saved....")

        except Exception as e:
            raise CustomException(e,sys)


if __name__ == "__main__":
    obj = Scrape_Link()
    obj.initiate_scrape_link()