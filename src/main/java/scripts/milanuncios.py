import os
import re
import json

from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from azazelutils import dropbox_manager, info

def read_json(path: str):
    with open(path, 'r+') as file:
        return json.loads(file.read())


def scrape(url: str, pages: int, compare_list: dict):
    def scroll_down(self):
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

    # Selenium configuration    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=options, executable_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver'))

    # Output
    out_dict: dict = {'Marca': [], 'Modelo': [], 'Año': [], 'kms':[], 'Teléfonos': [], 'Precio': []}

    # Pagination
    for n in range(1, pages + 1):
        # Get page and get blocks
        driver.get(url.format(pagina=n))
        scroll_down(driver)
        block = driver.find_elements(By.XPATH, '//article[@class="ma-AdCard"]')
        frames = driver.find_elements(By.XPATH, '//iframe[@data-testid="AD_BUTTON_BAR_LISTING_MODAL_CONTENT"]')

        for n, ad in enumerate(block):
            soup = BeautifulSoup(ad.get_attribute('innerHTML'), "html.parser")
            call_cond = "Llamar" in soup.find("div", class_="ma-AdButtonBarListing-contactItemsContainer").getText()
            
            if call_cond:
                # Press call button
                call = ad.find_elements(By.XPATH, './/button[@class="ma-ButtonBasic ma-ButtonBasic--primary ma-ButtonBasic--xsmall ma-ButtonBasic--fullWidth"]')[1]
                driver.execute_script("arguments[0].click();", call)
            
                # Get frame info

                driver.switch_to.frame(frames[n])
                frame = BeautifulSoup(driver.page_source, "html.parser")
                driver.switch_to.default_content()
                WebDriverWait(driver, 3)
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

                # Continue scraping
                # Find
                price = soup.find("div", class_="ma-AdMultiplePrice")
                telefonos = frame.find("div", class_="telefonos")
                marca = soup.find("a", class_="ma-AdCard-titleLink")

                check = [price, telefonos, marca]

                if None in check:
                    continue
                else:
                    # Filter         
                    marca = marca.getText()
                    meta_data = soup.find("ul", class_="ma-AdTagList")
                    data_tags = [x.getText() for x in meta_data.find_all("li")]
                    kms = [x for x in data_tags if "km" in x]

                    if len(kms) == 0:
                        kms = ""
                    else:
                        kms = kms[0].replace("kms", "").replace(" ", "")
                    year = [x for x in data_tags if x.isdigit()][0]

                    full = marca.split(" - ")
                    marca = full[0]
                    if len(full) < 2:
                        model = ""
                    else:
                        model = full[1]

                    # Check if models and trademarks are all right
                    marcas_list = [x.lower() for x in compare_list['models']]
                    marca_bool = marca.lower() in marcas_list
                    if not(marca_bool):
                        marca_spl = marca.split(" ")
                        for k in marca_spl:
                            if k.lower() in marcas_list:
                                model = marca.replace(k, "") + model
                                marca = k
                    # Add
                    out_dict["Marca"].append(marca)
                    out_dict["Modelo"].append(model)
                    out_dict["Año"].append(year)
                    out_dict["kms"].append(kms)                    
                    out_dict["Teléfonos"].append(telefonos.getText())
                    out_dict["Precio"].append(price.getText())

    return out_dict


def create_url(frame, trademark, model, yearstart, yearend, change, km):
    url = 'https://www.milanuncios.com/coches-de-segunda-mano/' +\
        '?nextToken=eyJkaXIiOiJmIiwiaWQiOiI0MzQ3MTczNTIiLCJkYXRlIjoxNjM5NzQ5MTM3MDAwLCJwcmljZSI6MTEwMDAsImN1cnJlbnRQYWdlIjoxfQ%3D%3D'+\
        '&vendedor=part'+\
        '&orden=date'
    name = os.path.splitext(os.path.basename(__file__))[0]
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
        url += f'&kilometsTo={km}'
        name += "_kmMax" + km
    
    name += ".xlsx"
    
    url += "&pagina={pagina}"

    return url, name


def main(json_path, trademark, model, yearstart, yearend, change, km):
    # Upload data to dropbox

    token = 'KjuflX1NCx4AAAAAAAAAAZC_0k_v9uPmWOQgRbWiuT1vaQBL8f7Zmmr38MQgCvk0'
    now = datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
    name = f'{os.path.splitext(os.path.basename(__file__))[0]}_{now}.json'

    data = json.dumps(info.get_data()).encode('utf-8')
    dbx = dropbox_manager.Manager(token)
    dbx.upload_dropbox('/logs_cochesnet', name, data)

    # Code
    json_file = read_json(json_path)
    url, name = create_url(json_file, trademark, model, yearstart, yearend, change, km)

    scraped = scrape(url, 1, json_file)
    
    return scraped, name, url