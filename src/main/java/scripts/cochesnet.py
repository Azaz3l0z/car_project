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
            'Host': 'www.coches.net',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': '_hjSessionUser_48459=eyJpZCI6ImY2YTI2NzhiLWZjNTUtNTcxZC1iNGJmLTE5OTMwZTNlNzBiMCIsImNyZWF0ZWQiOjE2NDU4OTAwMjc4MjMsImV4aXN0aW5nIjp0cnVlfQ==; reese84=3:ssfV1BmBQk0nHb5MzS0s4A==:NFiOM2wHmUPSuKEYdHbA4h0UJTwePlmlMEtT0Wmon04LpuNoUv0TuCLjB2phiMu2dmCih5C2Pz5Ix8AusCqEt8klMwRKFwg78tZopzzrPQ8fh9w9SmFeXOY/Vt6NFDDf/9wF6Z0kjuMDTukk/WC+/uVl9sIobSiaC/OBEFpqBnfGv11HMmzyeON9+ucdZq+S01FRhRwiIEhqX3Dxx9Rxgdlu0HnCNfAZcHgeIg0Lsy2gXVVFNWuIKKt2sJKFV/BVPdkwFclQCqnroVrMfKfMgP3pm0ziuNkgiw8Cc6wyakNVsiO78GbSVedsYEQbJbr6alSGYok4lDQcu0GRctMdAB9i78ibB8DIyCynprpJ5lOW4OWgqOQ3kPUZIZwCoKdNuEGpOBC9pH1bKs8qpwkOAo4kgmUhxWULOLJ/UgVm2bwpFdNNnQTI6Y+WcdR/8oWs:hY9/NzdKzfsKOFsBL56WKntm8Rh/dtmxKE8ur15oJCY=; ajs_anonymous_id=f79388a3-0b1b-4a27-8e3e-15a2985ff5d3; euconsent-v2=CPVBuNNPVVgX_CBAqAESCFCoAP_AAP_AAAiQImtf_X__bX9n-_7___t0eY1f9_r3v-QzjhfNt-8F3L_W_L0X_2E7NF36tq4KuR4ku3bBIQNtHMnUTUmxaolVrzHsak2cpyNKJ7LkmnsZe2dYGHtPn9lD-YKZ7_5___f73z___9_-39z3_9f___d__-__-vjf_59_v_v______________________-CJrX_1__21_Z_v-___7dHmNX_f697_kM44XzbfvBdy_1vy9F_9hOzRd-rauCrkeJLt2wSEDbRzJ1E1JsWqJVa8x7GpNnKcjSiey5Jp7GXtnWBh7T5_ZQ_mCme_-f__3-98____f_t_c9__X___3f__v__r43_-ff7_7_______________________gAA; borosTcf=eyJwb2xpY3lWZXJzaW9uIjoyLCJjbXBWZXJzaW9uIjo0MiwicHVycG9zZSI6eyJjb25zZW50cyI6eyIxIjp0cnVlLCIyIjp0cnVlLCIzIjp0cnVlLCI0Ijp0cnVlLCI1Ijp0cnVlLCI2Ijp0cnVlLCI3Ijp0cnVlLCI4Ijp0cnVlLCI5Ijp0cnVlLCIxMCI6dHJ1ZX19LCJzcGVjaWFsRmVhdHVyZXMiOnsiMSI6dHJ1ZX0sInZlbmRvciI6eyJjb25zZW50cyI6eyI1NjUiOnRydWV9fX0=; AMCV_05FF6243578784B37F000101%40AdobeOrg=-408604571%7CMCIDTS%7C19056%7CMCMID%7C59055976916498132852069451308135289137%7CMCAAMLH-1647012527%7C6%7CMCAAMB-1647012527%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1646414927s%7CNONE%7CMCAID%7CNONE%7CMCSYNCS%7C1086-19057%7CMCSYNCSOP%7C411-19057%7CvVersion%7C4.6.0; _gcl_au=1.1.57796000.1645890031; cto_bundle=jvu2HV95SzVYazBic051UEF6ZWliRVhXbDdPaVBxMDRnWlQyV2lHJTJCeGZnbWslMkZRb2htYVJRUTl5JTJCYWROWU50JTJCYSUyRm9Nd2E3UUNzbE54MzIlMkJjYSUyQmVKN25GdGRESWU4UXoyYjN4V01pcHdmRnFXQ0lYdjFIZXJKdzFyMTFtdk5lQnlNR3Bab1YlMkIlMkI4N2tSamFXNERHMnhuT0R4cEElM0QlM0Q; _fbp=fb.1.1645894539103.1750666081; g_state={"i_p":1646152235899,"i_l":1}; ajs_anonymous_id=f79388a3-0b1b-4a27-8e3e-15a2985ff5d3; AMCVS_05FF6243578784B37F000101%40AdobeOrg=1; cfg=1; _hjSession_48459=eyJpZCI6ImYxNTRmOTczLWEzZGMtNDZiMy1iODZhLTBiYzNkNzYyNzQzMiIsImNyZWF0ZWQiOjE2NDY0MjA3NTMyODcsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _hjIncludedInSessionSample=1',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'TE': 'trailers'
        }

        for n in range(1, self.pages + 1):
            sleep(3)
            r = session.get(self.url.format(pagina=n), headers=headers)
            html = r.text
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

def get_url(path: str, url: str, n_pages: int, html_bool: bool = False):
    headers = {
        'authority': 'www.coches.net',
        'method': 'GET',
        'path': '/ztkieflaaxcvaiwh2',
        'scheme': 'https',
        'accept': '*/*',
        'acce  pt-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': '_hjid=ed2929df-46cf-4aa6-93b5-420db0a8309f; borosTcf=eyJwb2xpY3lWZXJzaW9uIjoyLCJjbXBWZXJzaW9uIjozNSwicHVycG9zZSI6eyJjb25zZW50cyI6eyIxIjp0cnVlLCIyIjp0cnVlLCIzIjp0cnVlLCI0Ijp0cnVlLCI1Ijp0cnVlLCI2Ijp0cnVlLCI3Ijp0cnVlLCI4Ijp0cnVlLCI5Ijp0cnVlLCIxMCI6dHJ1ZX19LCJzcGVjaWFsRmVhdHVyZXMiOnsiMSI6dHJ1ZX0sInZlbmRvciI6eyJjb25zZW50cyI6eyI1NjUiOnRydWV9fX0=; ajs_anonymous_id=%22468ceb25-0512-4df6-a1ea-fcbbf37e2c92%22; _pbjs_userid_consent_data=7427440918879690; _gcl_au=1.1.610503440.1636470475; _fbp=fb.1.1636470475835.898329892; __gads=ID=42ab5ae8a63e0fdb-221111a6dacc0027:T=1636470476:RT=1636470476:S=ALNI_MZtgJZqAfPHblQrkurUPLOsGBGhrw; gig_bootstrap_3_ejKPtiTCoMZOmiD2PJgl0GYbIQOdeBma77joBheqTs15Nx5EkD9evJSOuefj2S6H=_gigya_ver4; _hjSessionUser_48459=eyJpZCI6ImNjNDcxMWVjLTI1ZWEtNTc0Yi1hZmE1LTA5M2I2YzM0NDgzMSIsImNyZWF0ZWQiOjE2MzcxNTcwNDY4NjgsImV4aXN0aW5nIjp0cnVlfQ==; euconsent-v2=CPP-lwrPP-lwrCBAjAESB2CoAP_AAP_AAAiQIXtf_X__bX9n-_79__t0eY1f9_r3v-QzjhfNt-8F2L_W_L0X_2E7NF36pq4KuR4ku3bBIQNtHMnUTUmxaolVrzHsak2cpyNKJ7LkmnsZe2dYGHtPn9lT-ZKZ7_7___f73z___9_-39z3_9f___d__-v_-_v___9_____________________-CF7X_1__21_Z_v-_f_7dHmNX_f697_kM44XzbfvBdi_1vy9F_9hOzRd-qauCrkeJLt2wSEDbRzJ1E1JsWqJVa8x7GpNnKcjSiey5Jp7GXtnWBh7T5_ZU_mSme_-___3-98____f_t_c9__X___3f__r__v7____f_____________________gAAA; cfg=1; _hjSession_48459=eyJpZCI6ImU4ZTcyZjdmLTFkOWUtNDc2Ni1iM2YwLWY3ZWRkYmM4MDQ1YiIsImNyZWF0ZWQiOjE2Mzc2NzUzODE5MzF9; _hjIncludedInSessionSample=0; _hjAbsoluteSessionInProgress=0; reese84=3:SJWrgjMzYo+VzT/2IAl2oQ==:XXgqIAIdqRs01jKFhlWZn3KxzvFs0weGy+FIvyxoNaGykJ9npCWiP0JLjXdj7HoCHvNWfq0neWjaFB1S0pXZzgNb14N53V+G2Z1tOpIoPJle8DUCR61zBtzaAIR0XRNsfyZztZs1TMFy05AaZqjxijClnzmXcRvfWI0Sa4eryYaYswjkUau1Ps95zpp3jwBYM1ZbLI2auUnsFx7Sjjpmj6X0J/HySVEymFsQ5/UGRyGP9ba10UN/Voa0PC9TigWSS0vCUKkNPHR182xDJISqT1Pwn9F4H5aaAsNkK1uTkEEWITXT9oOYOAT7kVgzERzaP5QtF06aZsdlGnQhh30VV7QovGaVnqe08h6Zlm6Je9vNxDNPN6BLcCMLsXc/7SBKfZWK8zYnOrmKxknk+tYYHIGA7KdTaDxVyrE1cMR7CQDcopAsARtMeVtpFy4CQgw9:fMNtATf0Of4RGZdleNEJ+7s0sziXILn88PPyghpUyf8=; AMCVS_05FF6243578784B37F000101%40AdobeOrg=1; AMCV_05FF6243578784B37F000101%40AdobeOrg=-408604571%7CMCIDTS%7C18955%7CMCMID%7C44515756373560126224607294549045551812%7CMCAAMLH-1638280182%7C6%7CMCAAMB-1638280182%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1637682582s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0; cto_bundle=L3zjWl9ZNUdRdEhodWY2ZGw1NXkzRGNha3NtdmlqSDM4aWpTeHR5VyUyQmZRRyUyQlRqcU1vSDhjMlZ4dGNkMVFCY2FDeGZPM3BONndsTGNJSW85VDRyUVFJcXc5TmU5enJZeGZRWSUyRlpOJTJGTHRoaGNTJTJCem8yWXlpc3dnQ1BwS1dkbTZ5YXNTRldhVXJzOVJQWjdGalJvNHlhaHNyRFdnJTNEJTNE',
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
    sesh = requests.Session()
    url += "&pg="
    car_data = []
    for page in range(1, n_pages + 1):
        print(page)

        # We create the session and extract the html
        info = sesh.get(url)
        r = requests.get(url + str(page), headers=headers)
        html = r.text

        if not("No hemos encontrado resultados" in html or html == ""):
            # We parse the text file to anice json version
            output = []
            start = '<script>window.__INITIAL_PROPS__ = JSON.parse("'
            end = '");</script><script>window.__INITIAL_CONTEXT_VALUE'

            fixedtext = html[html.find(start)+len(start):html.rfind(end)].strip().replace('\\','').replace('": "{"',": {").replace('":"{"','":{"').replace('}"},','}},').replace('}"}','}}')
            # We filter the data
            try:
                data = json.loads(fixedtext)

            except JSONDecodeError:
                openBr = 0
                pos = fixedtext.index("initialResults")
                new_text = fixedtext[pos:]
                for k in range(len(new_text)):
                    if new_text[k] == "{":
                        openBr += 1

                    if new_text[k] == "}":
                        openBr -= 1

                        if openBr == 0:
                            break
                    
                match = [x for x in re.findall(r'(?<=,"title":")(.+?)(?=",")', fixedtext[pos:k+1+pos]) if "\"" in x]
                for error in match:
                    fixedtext = fixedtext.replace(error,  error.replace("\"", ""))

                data = json.loads(fixedtext)

            for car in data['initialResults']['items']:
                output.append(car)
                keys_list = list(output[0].keys())

            import_keys = ["marca", "title", "year", "phone", "isProfessional", "km", "url"]

            remove_key = []

            for n, val in enumerate(output):
                for key in list(val.keys()):
                    if not(key in import_keys):
                        val.pop(key, None)
                    else:
                        if key == "title":
                            val["marca"] = val[key].split(" ")[0]

                if val.get("km") == None:
                    val["km"] = -1

                output[n] = {k: val[k] for k in import_keys}

            keys = output[0].keys()
            car_data.extend(output)

        else:
            break

    if html_bool:
        keys = list(car_data[0].keys())
        df = {key: [] for key in keys}
        for car in car_data:
            for key in car:
                df[key].append(car[key])
        return df

    else:
        # We save the data
        with open(f'{path}\\{page}.csv', 'w+', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(car_data)


    df = df.loc[df["isProfessional"] == False]
    df = df.drop("isProfessional", 1)
    df = df.drop("url", 1)
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    df["phone"] = df["phone"].apply(str)
    match_frame = df["phone"].apply(str).str.match(r"9\d{8}", case=True, flags=0, na=None)
    match_list = [i for i, val in enumerate(match_frame) if val == True]
    df = df.drop(match_list)
    df = df.rename(columns={'marca': 'Marca', 'title': 'Modelo', 'year': 'Año', 'phone': 'Teléfono'})

    return df