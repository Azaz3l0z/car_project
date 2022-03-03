import os
import re
import json
import requests

from bs4 import BeautifulSoup

url = 'https://www.autoscout24.es/lst/' + \
    '{marca}/'+\
    '?sort=standard&desc=0&custtype=P&ustate=N%2CU&size=20&page=1&atype=C&'
r = requests.get(url.format(marca=""))
json_file = {'models': {}, 'time': []}

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

for marca in json_data:
    json_file['models'][marca['label']] = {'id': marca['id'], 'models': {}}
    r = requests.get(url.format(marca=marca['label']))
    

print(json_file.keys())


quit()

with open('test.txt', 'w') as file:
    file.write(json.dumps(json_data))
