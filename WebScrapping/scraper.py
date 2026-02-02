import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

class Scrapper:
    def __init__(self):
        self.TITLE = []
        self.UNDER_TITLE = []
        self.PRICE = []
        self.ADDRESS = []
        self.DATE = []
        self.KEY_VALUE = []
        self.PROPERTY_DETAIL_DESCRIPTION = []
        self.start = 0
        self.pages = 536
        self.save_file_path = 'Scrapped_Data/dataset.csv'

        if os.path.exists("Stopped_Data"):
            file = os.listdir("Stopped_Data")
            self.start = int(sorted(file)[-1].split('l')[-1].replace(".csv",""))
        
    def initiate_web_scraping(self):
        print("Initiating _Web_scraping")
        try:
            for i in range(self.start+1,(self.pages)+1):
                url = f"https://shweproperty.com/en/property/search/for-sale/all/all/all/min-max?&page={i}"
                self.stoped_file_path = f'Stopped_Data/till{i}.csv'
                main_page = requests.get(url).text
                main_page_soup = BeautifulSoup(main_page , 'html.parser')

                container = main_page_soup.find(class_ = 'twelve wide column')
                blocks  = container.find_all(class_ = "serp__block")

                links = []

                

                for j in blocks:
                    links.append(j.find('a').get('href'))

                # for no,link in enumerate(links,len(links)):
                #     print(link)
                #     house = requests.get(link).text

                total = len(links)
                for no, link in enumerate(links, 1):
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
                print(f"Complete_page_number -- > {i}")
                    
            os.makedirs(os.path.dirname(self.save_file_path),exist_ok=True)

            df= pd.DataFrame({"title":self.TITLE , 'undertitle':self.UNDER_TITLE,
                                      "price":self.PRICE, "address":self.ADDRESS ,
                                      "date":self.DATE , "key_value":self.KEY_VALUE , 
                                      "propertydetail":self.PROPERTY_DETAIL_DESCRIPTION})
            df.to_csv(self.save_file_path , index=False , header=True)

            return df.shape
            

        finally:
            os.makedirs(os.path.dirname(self.stoped_file_path),exist_ok=True)
            df= pd.DataFrame({"title":self.TITLE , 'undertitle':self.UNDER_TITLE,
                                      "price":self.PRICE, "address":self.ADDRESS ,
                                      "date":self.DATE , "key_value":self.KEY_VALUE , 
                                      "propertydetail":self.PROPERTY_DETAIL_DESCRIPTION})
            df.to_csv(self.stoped_file_path, index=False , header=True)



if __name__ == "__main__":
    s = Scrapper()
    shape = s.initiate_web_scraping()
    print(shape)
