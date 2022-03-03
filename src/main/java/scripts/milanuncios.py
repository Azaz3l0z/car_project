import os
import re
import json

from bs4 import BeautifulSoup
from threading import Thread
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def read_json(path: str):
    with open(path, 'r+') as file:
        return json.loads(file.read())


def create_url(frame, trademark, model, yearstart, yearend, change, km):
    # Definitions
    url = 'https://www.milanuncios.com/coches-de-segunda-mano/' +\
        '?'+\
        '&vendedor=part'+\
        '&orden=date'
    name = os.path.splitext(os.path.basename(__file__))[0]

    # Create url and file_name
    if trademark != "Marca":
        url += f'&marca={frame["models"][trademark]["id"]}'
        name += "_" + trademark

    if model != "Modelo":
        url += f'&modelo={frame["models"][trademark]["models"][model]}'
        name += "_" + model

    if yearstart != "Año":
        url += f'&anod={yearstart}'
        name += "_" + yearstart
    
    if yearend != "Año":
        url += f'&anoh={yearend}'
        name += "_" + yearend

    if change != "Cambio":
        url += f'&cajacambio={change.lower()}'
        name += "_" + change
    
    if (km != "Hastaxkm") and (km != ""):
        url += f'&kilometersTo={km}'
        name += "_kmMax" + km
    
    name += ".csv"
    url += "&pagina={pagina}"

    return url, name


class Scraper(object):
    def __init__(self, url: str, pages: int, compare_list: dict, chromedriver_path: str) -> None:
        self.url = url
        self.pages = pages
        self.json_file = compare_list
        self.chromedriver_path = chromedriver_path
        self.data_dict: dict = {}
        self.ads: list = []

        self.create_soup()
        self.filter_ads()
        self.doAll()

    def doAll(self):
        th_phone = Thread(target=self.get_phone, daemon=True)
        th_phone.start()
        self.get_trademark_and_model()
        self.get_tagList_items()
        th_phone.join()
        self.get_url()

    def close(self):
        self.driver.close()

    def create_soup(self):
        # Selenium configuration    
        options = Options()

        options.add_argument("--headless")
        options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(executable_path='chromedriver', options=options)
        # NOTE: Care for the chromedriver file being installed properply. This version
        #       works even when Chrome is not installed. It you use Service() you need
        #       Chrome binaries installed

        # We paginate over n pages and get a selenium html object
        for n in range(1, self.pages + 1):
            print(n)
            self.driver.get(self.url.format(pagina=n))
            self.scroll_down(self.driver)
            if '¡Vaya! Han volado los anuncios' in self.driver.page_source:
                break
            else:
                for ad in self.driver.find_elements(By.XPATH, '//article[@class="ma-AdCard"]'):
                    self.ads.append(BeautifulSoup(ad.get_attribute('innerHTML'), "html.parser"))

    def filter_ads(self):
        # We filter if its a new car (we are not interested) or if we can't get the phone number
        for n, ad in enumerate(self.ads):
            if ad.find("li", {'data-testid': 'AD_BUTTON_BAR_LISTING_CONTACT_CALL'}) == None:
                self.ads[n] = None

            elif ad.find("p", class_="ma-AdCard-tag ma-AdCard-newAdTag") != None:
                self.ads[n] = None
        self.ads.append(None)
        self.ads = list(set(self.ads))
        self.ads.pop(self.ads.index(None))
    
    def get_phone(self):
        self.phone = []
        iframe_url = 'https://www.milanuncios.com/datos-contacto/?usePhoneProxy=0&from=list&includeEmail=false&id={id}'
        for ad in self.ads:
            id = ad.find("p", class_="ma-AdCard-adId").getText()
            self.driver.get(iframe_url.format(id=id))
            phone = self.driver.find_element(By.XPATH, '//div[@class="telefonos"]').text
            self.phone.append(phone)
        
        self.data_dict["Teléfonos"] = self.phone

    def get_url(self):
        self.urls = []
        og_url = 'https://www.milanuncios.com'
        for ad in self.ads:
            url = ad.find("a", class_="ma-AdCard-titleLink")["href"]
            self.urls.append(og_url + url)
        
        self.data_dict["Url"] = self.urls

    def get_trademark_and_model(self):
        self.trademark = []
        self.model = []
        for ad in self.ads:
            title: str = ad.find("a", class_="ma-AdCard-titleLink").getText()
            if title.count("-") >= 1:
                title = title.split(" - ")
                title = list(map(lambda x: re.search(r'(?<=^\s)?\w+\-?\s?\w+', x).group(), title))
                trademark, model = title

            elif title.count("-") == 0:
                pass

            self.trademark.append(trademark)
            self.model.append(model)
        
        self.data_dict['Marcas'] = self.trademark
        self.data_dict['Modelos'] = self.model
        
    def get_price(self):
        self.price = []
        for ad in self.ads:
            price = ad.find("span", class_="ma-AdPrice-value ma-AdPrice-value--default ma-AdPrice-value--heading--m").getText()
            self.price.append(price)

        self.data_dict['Precio'] = self.price

    def get_tagList_items(self):
        self.km = []
        self.year = []
        self.change = []
        for ad in self.ads:
            tagList = ad.find("ul", class_="ma-AdTagList")
            tagList = tagList.find_all("li")
            km = ""
            change = ""
            year = ""
            for tag in tagList:
                txt = tag.getText()
                # We get kms
                if "kms" in txt:
                    km = txt
                # We get change
                if txt in ["Manual", "Automático"]:
                    change = txt
                # We get year
                if len(txt) == 4 and txt.isdigit():
                    year = txt
            self.km.append(km)
            self.year.append(year)
            self.change.append(change)

        self.data_dict['Año'] = self.year
        self.data_dict['Cambio'] = self.change
        self.data_dict['Km'] = self.km

    @staticmethod
    def scroll_down(driver):
        """A method for scrolling the page."""
        # Get scroll height.
        last_height = driver.execute_script("return document.body.scrollHeight")
        y = 0

        while True:
                y += 500

                # Scroll down to the bottom.
                driver.execute_script(f"window.scrollTo(0, {y})") 

                sleep(0.01)

                # Calculate new scroll height and compare with last scroll height.
                new_height = driver.execute_script("return document.body.scrollHeight")

                if y >= last_height:
                    break

                last_height = new_height


def main(json_path, trademark, model, yearstart, yearend, change, km):
    # Code
    json_file = read_json(json_path)
    chrom_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver')
    url, name = create_url(json_file, trademark, model, yearstart, yearend, change, km)
    
    with open(os.path.join(os.path.dirname(json_path), 'name.txt'), 'w+') as file:
        file.write(name)

    scrpr = Scraper(url, 10, json_file, chrom_path)
    scrpr.close()
    
    return scrpr.data_dict, name, url

    