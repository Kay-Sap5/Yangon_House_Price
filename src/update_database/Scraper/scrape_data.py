from src.logging.logger import logging
from src.exception.exception import CustomException
import requests
from bs4 import BeautifulSoup
import os
import sys
import pandas as pd
from src.update_database.scraper_artifact.scraper_artifact import ScrapeNewLinkArtifact,ScrapeDataArtifact

class ScrapData:
    def __init__(self , srcape_new_link_artifact : ScrapeNewLinkArtifact):
        logging.info("Entered ScrapData")
        try:
            self.scrape_new_link_artifact = srcape_new_link_artifact
            self.TITLE = []
            self.UNDER_TITLE = []
            self.PRICE = []
            self.ADDRESS = []
            self.DATE = []
            self.KEY_VALUE = []
            self.PROPERTY_DETAIL_DESCRIPTION = []
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_scrap_data(self) -> ScrapeDataArtifact:
        logging.info("Enterd initiate_scrap_data")
        try:
            for link in self.scrape_new_link_artifact.new_links:
                    # print(f"Scraping {no}/{total}")
                    house = requests.get(link).text
                    
                    house_soup = BeautifulSoup(house,'html.parser')

                    title = house_soup.find("h1").text
                    self.TITLE.append(title)

                    under_title = house_soup.find("p",class_ = 'property__about-title').text
                    self.UNDER_TITLE.append(under_title)

                    address_and_price = house_soup.find(class_ = 'property__about-prehead')
                    address = address_and_price.find('p',class_ ='property__about-title' ).text.strip()
                    self.ADDRESS.append(address)

                    price = address_and_price.find("p",class_ = 'property__about-subtitle').text.strip()
                    self.PRICE.append(price)

                    date = house_soup.find('div' , class_ = 'm-text-right').text.strip()
                    self.DATE.append(date)
                    
                    property_detail_description = house_soup.find("p",class_ = 'property__details-subtitle').text
                    self.PROPERTY_DETAIL_DESCRIPTION.append(property_detail_description)

                    key_value = house_soup.find("ul")
                    key = key_value.find_all('p')
                    key_value_column = []
                    for k in list(key):
                        data = str(k).replace('<p>','').replace("</p>","")
                        key_value_column.append(data)

                    key_value_data = [] 
                    value = key_value.find_all("span")
                    for val in list(value):
                        data = str(val).replace("<span>","").replace("</span>","").strip()
                        key_value_data.append(data)
                    
                    self.KEY_VALUE.append(list((zip(key_value_column , key_value_data))))
            df= pd.DataFrame({"title":self.TITLE , 'undertitle':self.UNDER_TITLE,
                                      "price":self.PRICE, "address":self.ADDRESS ,
                                      "date":self.DATE , "key_value":self.KEY_VALUE , 
                                      "propertydetail":self.PROPERTY_DETAIL_DESCRIPTION})
            logging.info(f"New Data Frame Shape => {df.shape}")
            scrape_data_artifact = ScrapeDataArtifact(df)
            return scrape_data_artifact

        except Exception as e:
            raise CustomException(e,sys)
        