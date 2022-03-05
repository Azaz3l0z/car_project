import os
import re
import json
import queue
import requests
import pandas as pd

import threading
from bs4 import BeautifulSoup

# Worker thread
class Worker(threading.Thread):
    def __init__(self, queue, p_list, *args, **kwargs):
        self.queue = queue
        self.p_list = p_list

        super().__init__(*args, **kwargs)
        self.daemon = True

    def run(self):
        while True:
            try:
                url, n = self.queue.get(timeout=5)  # 3s timeout
            except queue.Empty:
                return

            # do whatever work you have to do on work
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            phone = soup.find("a", {"id": "js-original-phone-number"})

            if phone != None:
                phone = phone.getText()
                phone = phone[::-1]
                phone = phone.replace(' ', '')
                phone = phone.replace('-', '')
                phone = phone[:9][::-1]

            self.p_list.append({n: phone})
            print({n: phone})
            # End
            self.queue.task_done()

# Scraper Class
class Scraper(object):
    def __init__(self, url: str, pages: int, compare_list: dict) -> None:
        self.url = url
        self.pages = pages
        self.json_file = compare_list
        self.keys = ['Marca', 'Modelo', 'Año', 'Km', 'Cambio', 'Teléfono', 'URL']
        self.data_dict: dict = {}
        self.ads: list = []

        self.create_soup()
        self.doAll()

    def doAll(self):
        th = threading.Thread(target=self.get_phones_and_url, daemon=True)
        th.start()
        self.get_trademark_and_model()
        self.get_tagList_items()
        th.join()
        self.filter()
        self.sort()

    def create_soup(self):
        self.session = requests.Session()

        for k in range(1, self.pages + 1):
            print(k)
            r = self.session.get(self.url.format(pagina=k))
            try:
                soup = BeautifulSoup(r.text, 'html.parser')
                n_ofertas = soup.find("span", class_="sc-font-bold cl-filters-summary-counter").getText()
                n_ofertas = re.search(r'\d+', n_ofertas).group()
                print(n_ofertas)
                if 20*(k-1) >= int(n_ofertas):
                    break
                all_ads = soup.find("div", {"class": "cl-list-elements"})
                cards = all_ads.find_all("div", class_="cl-list-element cl-list-element-gap")
                self.ads.extend(cards)

            except AttributeError:
                break
    
    def get_phones_and_url(self):
        self.urls = []
        self.phone = []
        self.queue = queue.Queue()

        for n, ad in enumerate(self.ads):
            url = ad.find("a", {"data-item-name": "detail-page-link"}).attrs['href']
            url = 'https://www.autoscout24.es' + ad.find("a", {"data-item-name": "detail-page-link"}).attrs["href"]
            self.urls.append(url)
            self.queue.put([url, n])
        
        for n in range(5):
            Worker(self.queue, self.phone).start()

        self.data_dict['URL'] = self.urls
        self.queue.join()

        self.phone.sort(key=lambda x: next(iter(x.keys())))
        self.phone = [x[next(iter(x.keys()))] if 
            x[next(iter(x.keys()))] != None else None for x in self.phone]

        self.data_dict['Teléfono'] = self.phone   
        
    def get_trademark_and_model(self):
        self.trademark = []
        self.model = []

        for ad in self.ads:
            txt = ad.find("h2", {"class": "cldt-summary-makemodel sc-font-bold sc-ellipsis"}).getText()
            txt = txt.split()
            trademark = ""
            model = ""

            for n, word in enumerate(txt):
                trademark += word
                if trademark in self.json_file['models']:
                    model = " ".join(txt[n+1:])
                    break
                else:
                    trademark += " "

            self.trademark.append(trademark)
            self.model.append(model)
        
        self.data_dict['Marca'] = self.trademark
        self.data_dict['Modelo'] = self.model
             
    def get_tagList_items(self):
        self.km = []
        self.year = []
        self.change = []

        for k, ad in enumerate(self.ads):
            ul = ad.find("ul", {"data-item-name": "vehicle-details"})
            
            km = ul.find("li", {"data-type": "mileage"}).getText()
            year = ul.find("li", {"data-type": "first-registration"}).getText()
            change = ul.find("li", {"data-type": 
                "transmission-type"}).getText()
            
            if 'km' in km:
                km = re.match(r'\d+', 
                    km.replace('\n', '').replace('.', '').replace('km', 
                    '')).group()
            year = re.search(r'\d{4}', year).group()
            change = change.replace('\n', '').replace('- (Cambio)', '')

            self.km.append(km)
            self.year.append(year)
            self.change.append(change)
        
        self.data_dict['Km'] = self.km
        self.data_dict['Año'] = self.year
        self.data_dict['Cambio'] = self.change

    def filter(self):
        df = pd.DataFrame(self.data_dict)
        for n, phone in enumerate(df['Teléfono']):
            if phone == None:
                df = df.drop([n])

        self.data_dict = df.to_dict('list')

    def fix_kms(self, kms):
        df = pd.DataFrame(self.data_dict)
        for n, km in enumerate(df['Km']):
            if int(km) > int(kms):
                df = df.drop([n])

        self.data_dict = df.to_dict('list')

    def sort(self):
        self.data_dict = {x: self.data_dict[x] for x in self.keys}            


# First we read the json
def read_json(path: str):
    with open(path, 'r+') as file:
        return json.loads(file.read())


def create_url(frame, trademark, model, yearstart, yearend, change, km):
    # Definitions
    url = 'https://www.autoscout24.es/lst/{marca}{{model}}' +\
        '?sort=age&desc=1' + \
        '&custtype=P&ustate=N%2CU&size=20&cy=E&atype=C&'
    name = os.path.splitext(os.path.basename(__file__))[0]

    # Create url and file_name
    if trademark != "Marca":
        url = url.format(marca=trademark+'/')
        name += "_" + trademark
    else:
        url = url.format(marca="")

    if model != "Modelo":
        url = url.format(model=model)
        name += "_" + model
    else:
        url = url.format(model="")

    if yearstart != "Desde":
        url += f'&fregfrom={yearstart}'
        name += "_" + yearstart
    
    if yearend != "Hasta":
        url += f'&fregto={yearend}'
        name += "_" + yearend

    if change != "Cambio":
        url += f'&gear={change[0]}'
        name += "_" + change
    
    if (km != "Hastaxkm") and (km != ""):
        all_kms = [0, 2500, 5000]
        all_kms.extend([x*10000 for x in range(1, 10)])
        all_kms.extend([100000*(1+k/len(range(1, 5))) for k in range(5)])
        for k in range(len(all_kms[:-1])):
            if all_kms[k] < int(km) < all_kms[k+1]:
                km = str(all_kms[k+1])
                break
        url += f'&kmto={km}'
        name += "_kmMax" + km
    
    name += ".csv"
    url += "&page={pagina}"

    return url, name


def main(json_path, trademark, model, yearstart, yearend, change, km):
    json_file = read_json(json_path)
    url, name = create_url(json_file, trademark, model, yearstart, yearend, 
        change, km)
    
    scrpr = Scraper(url, 10, json_file)
    if (km != 'Hastaxkm') and (km != ""):
        scrpr.fix_kms(km)

    return scrpr.data_dict, name, url