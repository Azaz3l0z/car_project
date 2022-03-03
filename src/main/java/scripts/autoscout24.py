import os
import re
import json
import requests

from threading import Thread
from bs4 import BeautifulSoup


# Scraper Class
class Scraper(object):
    def __init__(self, url: str, pages: int, compare_list: dict) -> None:
        self.url = url
        self.pages = pages
        self.json_file = compare_list

        self.data_dict: dict = {}
        self.ads: list = []

        self.create_soup()
        self.filter_ads()
        self.doAll()


# First we read the json
def read_json(path: str):
    with open(path, 'r+') as file:
        return json.loads(file.read())


def create_url(frame, trademark, model, yearstart, yearend, change, km):
    # Definitions
    url = 'https://www.autoscout24.es/lst/' +\
        '?sort=age&desc=1' + \
        '&custtype=P&ustate=N%2CU&size=20&page=1&atype=C&'
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


def main(json_path, trademark, model, yearstart, yearend, change, km):
    json_file = read_json(json_path)
    url, name = create_url(json_file, trademark, model, yearstart, yearend, 
        change, km)
        