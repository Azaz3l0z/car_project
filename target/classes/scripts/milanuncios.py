import os
import re
import json
import requests

class Scraper(object):
    def __init__(self, url: str, pages: int, compare_list: dict) -> None:
        self.url = url
        self.pages = pages
        self.json_file = compare_list
        self.keys = ['Marca', 'Modelo', 'Año', 'Km', 'Cambio', 'Teléfono', 'URL']
        self.data_dict: dict = {}
        self.ads: list = []

        self.get_ads()
        self.filter_ads()
        self.doAll()

    def doAll(self):
        self.get_phone()
        self.get_trademark_and_model()
        self.get_tagList_items()
        self.get_url()
        self.sort()

    def delete_tag(self, json_data: str, ini_str: str, end_str):
        while (ini_str in json_data):
            ini_idx = json_data.find(ini_str)
            end_idx = json_data[ini_idx:].find(end_str) + ini_idx + len(end_str) - 1
            json_data = json_data[:ini_idx]+json_data[end_idx:]

        return json_data

    def get_ads(self):
        # We paginate over n pages and get a the script that build the page
        session = requests.Session()
        start = '<script>window.__INITIAL_PROPS__ = JSON.parse("'
        end = '");</script><script>window.__INITIAL_CONTEXT_VALUE__ =' 

        for n in range(1, self.pages + 1):
            r = session.get(self.url.format(pagina=n))
            html = r.text

            if '¡Vaya! Han volado los anuncios' in html:
                break
            else:
                json_data = html[html.find(start) + len(start): 
                                html.find(end)]
                json_data = json_data.replace('\\', '')
                
                with open('test2.txt', 'w+') as file:
                    file.write(json_data)

                # We remove description tags (They cause many problems)

                json_data = self.delete_tag(json_data, '"description":', '","')
                json_data = self.delete_tag(json_data, '"seoTitle":', '","')
                

                json_data = re.sub(r'((?<![:,\[{])")(?![:\],}])', '', json_data)
                json_data = re.sub(r'\s\d{2}"', '', json_data)

                with open('test.txt', 'w+') as file:
                    file.write(json_data)
                
                
                          
                ads = json.loads(json_data)['adListPagination']['adList']['ads']
                
                self.ads.extend(ads)       

    def filter_ads(self):
        # We filter if its a new car (we are not interested) or if we can't get the phone number
        new_list = []
        for ad in self.ads:
            if 'firstPhoneNumber' in ad:
                new_list.append(ad)

        self.ads = new_list

    def get_phone(self):
        self.phone = []
        for ad in self.ads:
            phone = re.search(r'(?![34])\d{9}', ad['firstPhoneNumber']).group()
            self.phone.append(phone)
        
        self.data_dict['Teléfono'] = self.phone

    def get_url(self):
        self.urls = []
        og_url = 'https://www.milanuncios.com'
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
                    model = " ".join(title[n+1:]).replace('- ', 
                        '').lower().title()
                    break
                else:
                    trademark += " "
            self.trademark.append(trademark.title())
            self.model.append(model)

        self.data_dict['Marca'] = self.trademark
        self.data_dict['Modelo'] = self.model

    def get_tagList_items(self):
        self.km = []
        self.year = []
        self.change = []
        for ad in self.ads:
            tags = {x['type']: x['text'] for x in ad['tags']}
            km = ""
            change = ""
            year = ""

            if 'kms' in tags:
                km = tags['kms'].replace('kms', '').replace('.', '')
                km = re.search(r'\d+', km).group()

            if 'cambio' in tags:
                change = tags['cambio'].replace('u00E1', 'á')
            
            if 'au00F1o' in tags:
                year = tags['au00F1o']

            self.km.append(km)
            self.year.append(year)
            self.change.append(change)

        self.data_dict['Año'] = self.year
        self.data_dict['Cambio'] = self.change
        self.data_dict['Km'] = self.km

    def sort(self):
        self.data_dict = {x: self.data_dict[x] for x in self.keys}


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

    if yearstart != "Desde":
        url += f'&anod={yearstart}'
        name += "_" + yearstart
    
    if yearend != "Hasta":
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
    # Code
    json_file = read_json(json_path)
    url, name = create_url(json_file, trademark, model, yearstart, yearend, change, km)
    with open(os.path.join(os.path.dirname(json_path), 'name.txt'), 'w+') as file:
        file.write(name)
    
    scrpr = Scraper(url, 10, json_file)
    
    return scrpr.data_dict, name, url

    