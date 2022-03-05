import os
import re
import json
import requests

from time import sleep
from bs4 import BeautifulSoup

# Scraper Class
class Scraper(object):
    def __init__(self, url: str, pages: int, compare_list: dict, 
                    change) -> None:

        self.url = url
        self.pages = pages
        self.json_file = compare_list
        self.change_str = change

        self.keys = ['Marca', 'Modelo', 'Año', 'Km', 'Cambio', 'Teléfono', 'URL']
        self.data_dict: dict = {}
        self.ads: list = []

        self.get_ads()
        self.filter_ads()
        self.doAll()

    def doAll(self):
        self.get_phone()
        self.get_trademark_and_model()
        self.get_km_year()
        self.get_url()
        self.get_change()
        self.sort()

    def get_ads(self):
        # We paginate over n pages and get a the script that build the page
        session = requests.Session()
        start = '<script>window.__INITIAL_PROPS__ = JSON.parse("'
        end = '");</script><script>window.__INITIAL_CONTEXT_VALUE'

        headers = {
            'authority': 'www.coches.net',
            'method': 'GET',
            'path': '/ztkieflaaxcvaiwh2',
            'scheme': 'https',
            'accept': '*/*',
            'acce  pt-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'Cookie': 'ajs_anonymous_id=eb7e8458-69dc-4339-9ccf-9edde76ba2c8; ajs_anonymous_id=eb7e8458-69dc-4339-9ccf-9edde76ba2c8; cfg=1; reese84=3:7GcYIM7lx0DmJ5Y2hoj1qQ==:n0Cvq+w60I3JJi7Cy0trPkegOFxDqEDiw06psLS7hGtgTCdeeS0V6Y/2gZcHKUPh+bL4La+SMQPfzTZKdkHDYCroAL2GdFIMNP28+Wim3SCvchoDilYjZnR3sc0c/KYLP3/Lv6t4uOg9YFoUQvhd2K2BpIrCV32jRsJT8brfKH81dwGmcqElFKudzkubSDAwje0P0ixhEvKBXpptjs+tnwjWIjkVMjuOA0yQVva5C8FY2rW75LXKPA4ad5lLFLfo6XhfVyHtw6/77PrYQVYWYoKBQtMkCPFjHbEae5uA0oeYMNXx4PJZIC7qWgKTNvZUcr5YjWlXp+4Z3SukIiGoRlsOoqlK4RAt/h0q29xEd8RenF1+tjJ6xl3VKXFiTfauIAak5mvlWxxgPApZp9AscpGxt40GFWce2OG3zDkZ444caIVwHUZZ0PL2kXXSmzfT:sSzfb+A8+XQPKU+RJTQNiiNXkTyfM4G9eGM7DOmsr9g=; euconsent-v2=CPVWUPNPVWUPNCBAqAESCFCoAP_AAP_AAAiQImtf_X__bX9n-_7___t0eY1f9_r3v-QzjhfNt-8F3L_W_L0X_2E7NF36tq4KuR4ku3bBIQNtHMnUTUmxaolVrzHsak2cpyNKJ7LkmnsZe2dYGHtPn9lD-YKZ7_5___f73z___9_-39z3_9f___d__-__-vjf_59_v_v______________________-CJrX_1__21_Z_v-___7dHmNX_f697_kM44XzbfvBdy_1vy9F_9hOzRd-rauCrkeJLt2wSEDbRzJ1E1JsWqJVa8x7GpNnKcjSiey5Jp7GXtnWBh7T5_ZQ_mCme_-f__3-98____f_t_c9__X___3f__v__r43_-ff7_7_______________________gAA; borosTcf=eyJwb2xpY3lWZXJzaW9uIjoyLCJjbXBWZXJzaW9uIjo0MiwicHVycG9zZSI6eyJjb25zZW50cyI6eyIxIjp0cnVlLCIyIjp0cnVlLCIzIjp0cnVlLCI0Ijp0cnVlLCI1Ijp0cnVlLCI2Ijp0cnVlLCI3Ijp0cnVlLCI4Ijp0cnVlLCI5Ijp0cnVlLCIxMCI6dHJ1ZX19LCJzcGVjaWFsRmVhdHVyZXMiOnsiMSI6dHJ1ZX0sInZlbmRvciI6eyJjb25zZW50cyI6eyI1NjUiOnRydWV9fX0=; AMCV_05FF6243578784B37F000101%40AdobeOrg=-408604571%7CMCIDTS%7C19056%7CMCMID%7C03683581035080727250441421648136151517%7CMCAID%7CNONE%7CMCOPTOUT-1646437097s%7CNONE%7CvVersion%7C4.6.0; AMCVS_05FF6243578784B37F000101%40AdobeOrg=1; _gcl_au=1.1.1162216004.1646429897',
            'pragma': 'no-cache',
            'referer': 'https://www.coches.net/segunda-mano/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }

        for n in range(1, self.pages + 1):
            sleep(4)
            print(n)
            r = session.get(self.url.format(pagina=n), headers=headers)
            html = r.text
            with open('test.txt', 'w+') as file:
                file.write(html)
            soup = BeautifulSoup(html, 'html.parser')
            n_ads = soup.find("h1", {"class": "mt-TitleBasic-title mt-TitleBasic-title--xs mt-TitleBasic-title--black"}).getText()
            n_ads = re.match(r'\d+', n_ads).group()
            
            if 35*(n-1) > int(n_ads):
                break
            else:
                json_data = html[html.find(start) + len(start):html.rfind(end)]
                json_data = json_data.strip().replace('\\',
                    '').replace('": "{"',": {").replace('":"{"',
                    '":{"').replace('}"},','}},').replace('}"}','}}')

                ads = json.loads(json_data)['initialResults']['items']

                self.ads.extend(ads)                 

    def filter_ads(self):
        # We filter if its a new car (we are not interested) or if we can't get the phone number
        new_list = []
        for ad in self.ads:
            if 'phone' in ad:
                new_list.append(ad)

        self.ads = new_list

    def get_phone(self):
        self.phone = []
        for ad in self.ads:
            phone = re.search(r'(?![34])\d{9}', ad['phone']).group()
            self.phone.append(phone)
        
        self.data_dict['Teléfono'] = self.phone

    def get_url(self):
        self.urls = []
        og_url = 'https://www.coches.net'
        for ad in self.ads:
            self.urls.append(og_url + ad['url'])
        
        self.data_dict["URL"] = self.urls

    def get_trademark_and_model(self):
        self.trademark = []
        self.model = []
        keys = [x.lower() for x in self.json_file['models']]
        for ad in self.ads:
            title: str = ad['title']
            title = title.split()
            trademark = ""
            model = ""

            for n, word in enumerate(title):
                trademark += word
                if trademark.lower() in keys:
                    for k, word in enumerate(title[n+1:]):
                        model += word
                        if model in self.json_file['models'][trademark.upper()]['models']:
                            break
                        else:
                            model += " "
                    break
                else:
                    trademark += " "

            self.trademark.append(trademark.title())
            self.model.append(model)

        self.data_dict['Marca'] = self.trademark
        self.data_dict['Modelo'] = self.model

    def get_km_year(self):
        self.km = []
        self.year = []
        self.change = []
        for ad in self.ads:
            km = ""
            year = ""

            if 'km' in ad:
                km = ad['km']
            
            if 'year' in ad:
                year = ad['year']

            self.km.append(km)
            self.year.append(year)

        self.data_dict['Año'] = self.year
        self.data_dict['Km'] = self.km

    def get_change(self):
        if self.change_str == 'Cambio':
            self.change_str = ''

        self.change = []
        for _ in self.ads:
            self.change.append(self.change_str)
        
        self.data_dict['Cambio'] = self.change

    def sort(self):
        self.data_dict = {x: self.data_dict[x] for x in self.keys}


# First we read the json
def read_json(path: str):
    with open(path, 'r+') as file:
        return json.loads(file.read())

# We create the url for the scraper and the name of the output file
def create_url(frame, trademark, model, yearstart, yearend, change, km):
    # Definitions
    url = 'https://www.coches.net/segunda-mano/{marca}{{model}}' +\
        '?&st=2'
    name = os.path.splitext(os.path.basename(__file__))[0]

    # Create url and file_name
    if trademark != "Marca":
        url = url.format(marca=trademark+'/')
        name += "_" + trademark
    else:
        url = url.format(marca="")

    if model != "Modelo":
        url = url.format(model=model+'/')
        name += "_" + model
    else:
        url = url.format(model="")

    if yearstart != "Desde":
        url += f'&MinYear={yearstart}'
        name += "_" + yearstart
    
    if yearend != "Hasta":
        url += f'&MaxYear={yearend}'
        name += "_" + yearend

    if change != "Cambio":
        url += f'&gear={change[0]}'
        name += "_" + change
    
    if (km != "Hastaxkm") and (km != ""):
        cambios = ['A', 'M']
        url += f'&TransmissionTypeId={cambios.index[km[0]] + 1}'
        name += "_kmMax" + km
    
    name += ".csv"
    url += "&pg={pagina}"

    return url, name


def main(json_path, trademark, model, yearstart, yearend, change, km):
    json_file = read_json(json_path)
    url, name = create_url(json_file, trademark, model, yearstart, yearend, 
        change, km)

    scrpr = Scraper(url, 10, json_file, change)
    return scrpr.data_dict, name, url
