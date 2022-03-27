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

    def create_soup(self):
        self.session = requests.Session()
        for k in range(1, self.pages + 1):
            r = self.session.get(self.url.format(page=k))
            html = r.text
            try:
                soup = BeautifulSoup(html, 'html.parser')
                if k == 1:
                    n_ofertas = soup.find_all('as24-tracking')
                    for trackers in n_ofertas:
                        try:
                            if 'search_numberOfArticles' in trackers.attrs['as24-tracking-value']:
                                n_ofertas = json.loads(trackers.attrs['as24-tracking-value'])
                                n_ofertas = n_ofertas['search_numberOfArticles']
                        except:
                            pass

                if 20*(k-1) >= int(n_ofertas):
                    break

                ads = soup.find_all('div', {'class': 'cl-list-element cl-list-element-gap'})

                self.ads.extend(ads)

            except AttributeError:
                break

    def doAll(self):
        th = threading.Thread(target=self.get_phones_and_url, daemon=True)
        th.start()
        self.get_trademark_and_model()
        self.get_tagList_items()
        th.join()
        self.filter()
        self.sort()

    def get_phones_and_url(self):
        self.urls = []
        self.phone = []
        self.queue = queue.Queue()

        for n, ad in enumerate(self.ads):
            url = ad.find('a', {'data-item-name': 'detail-page-link'})
            url = url.attrs['href']
            url = 'https://www.autoscout24.es' + url

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
            title = ad.find('h2', 
                {'class': 'cldt-summary-makemodel sc-font-bold sc-ellipsis'})
            title = title.getText().split()
            txt = ''
            for word in title:
                txt += word
                if txt in self.json_file['models']:
                    trademark = txt
                    break
                else:
                    txt += ' '
            title = ' '.join(title)
            title = title.replace(trademark, '')

            model = title.strip()

            self.trademark.append(trademark)
            self.model.append(model)
        
        self.data_dict['Marca'] = self.trademark
        self.data_dict['Modelo'] = self.model
             
    def get_tagList_items(self):
        self.km = []
        self.year = []
        self.change = []

        for ad in self.ads:
            tags = ad.find('ul', {'data-item-name': 'vehicle-details'})

            km = tags.find('li', {'data-type': 'mileage'})
            year = tags.find('li', {'data-type': 'first-registration'})
            change = tags.find('li', {'data-type': 'transmission-type'})

            if km != None:
                km = km.getText()
                km = km.replace('.', '').replace(',', '').replace('km', '')
                km = km.strip()

            if year != None:
                year = re.search(r'\d{4}', year.get_text()).group().strip()

            if change != None:
                change = change.getText().strip()
                change = change.replace('- (Cambio)', '')

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

    def sort(self):
        self.data_dict = {x: self.data_dict[x] for x in self.keys}            

# First we read the json
def read_json(path: str):
    with open(path, 'r+') as file:
        return json.loads(file.read())

def create_url(frame, trademark, model, yearstart, yearend, change, km):
    # Definitions

    url = 'https://www.autoscout24.es/classified-list/react-listelements/es?='+\
        '&isSeoListPage=true'+\
        '&sort=age'+\
        '&desc=1'+\
        '&custtype=P'+\
        '&ustate=N,U'+\
        '&size=20'+\
        '&cy=E'+\
        '&mmm={marca}|{{model}}|'+\
        '&fregto=2019'+\
        '&atype=C'+\
        '&recommended_sorting_based_id=b62d0fbc-c44a-40cf-b2e9-23e3dc70fdb0'

    name = os.path.splitext(os.path.basename(__file__))[0]

    # Create url and file_name
    if trademark != "Marca":
        url = url.format(marca=frame['models'][trademark]['id'])
        name += "_" + trademark
    else:
        url = url.format(marca="")

    if model != "Modelo":
        url = url.format(model=frame['models'][trademark]['models'][model]['id'])
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
    url += "&page={page}"

    return url, name


def main(json_path, trademark, model, yearstart, yearend, change, km):
    json_file = read_json(json_path)
    url, name = create_url(json_file, trademark, model, yearstart, yearend, 
        change, km)
    
    scrpr = Scraper(url, 1000, json_file)

    return scrpr.data_dict, name, url