import os
import re
import json
import requests
import queue 
import threading
from time import sleep
from datetime import date, datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class Worker(threading.Thread):
    def __init__(self, queue, url, p_list, *args, **kwargs):
        self.queue = queue
        self.url = url
        self.p_list = p_list

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--log-level=3")

        super().__init__(*args, **kwargs)
        self.daemon = True
        self.driver = webdriver.Chrome(executable_path='chromedriver', options=options)

    def run(self):
        while True:
            try:
                work = self.queue.get(timeout=1)  # 3s timeout
            except queue.Empty:
                return

            # do whatever work you have to do on work
            self.driver.get(self.url.format(marca=work))
            html = self.driver.page_source
            find_str = 'availableModelModelLines" : ['
            start_idx = html.find(find_str)

            count = 1
            idx = start_idx + len(find_str)
            while (count != 0):
                if html[idx] == ']':
                    count -= 1
                if html[idx] == '[':
                    count += 1
                idx += 1
            print(work)
            self.p_list[work] = json.loads(html[start_idx - 1 + len(find_str):idx])
            
            # End
            self.queue.task_done()

class JSONDownloader(object):
    def __init__(self) -> None:
        self.url = 'https://www.autoscout24.es/lst/' + \
            '{marca}/'+\
            '?sort=age&desc=1&custtype=P&ustate=N%2CU&size=20&page=1&cy=E&atype=C&'
        self.json_file = {'models': {}, 'time': []}
        self.queue = queue.Queue()
        self.placeholder_list = {}

    def get_marcas(self):
        session = requests.Session()
        
        r = session.get(self.url.format(marca=""))
        html = r.text
        find_str = 'allMakes" : ['
        start_idx = html.find(find_str)

        count = 1
        idx = start_idx + len(find_str)
        while (count != 0):
            if html[idx] == ']':
                count -= 1
            if html[idx] == '[':
                count += 1
            idx += 1

        json_data = json.loads(html[start_idx - 1 + len(find_str):idx])[:-1]
        return json_data

    def get_models(self):
        json_data = self.get_marcas()

        for marca in json_data:
            self.queue.put(marca['label'])

        for k in range(10):
            Worker(self.queue, self.url, self.placeholder_list).start()

        self.queue.join()
        for marca in json_data:
            models = {}
            print(marca)
            for k in self.placeholder_list[marca['label']]:
                if k['isModel']:
                    models[k['name']] = k['id']
            self.json_file['models'][marca['label']] = {'id': marca['id'], 'models': models}

    def get_time(self):
        now = datetime.now().strftime('%Y')
        self.json_file['time'] = list(range(1900, int(now) + 1))

def main():
    json_data = JSONDownloader()
    json_data.get_time()
    json_data.get_models()

    with open('test.txt', 'w+') as file:
        file.write(json.dumps(json_data.json_file))

main()
