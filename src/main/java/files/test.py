import os
import json
import datetime

with open('milanuncios.json', 'r+') as file:
    data = json.loads(file.read())

data['time'] = []
end_year = int((datetime.datetime.now().strftime("%Y")))
ini_year = 1900

for k in range(ini_year, 1991, 10):
    data['time'].append(k)
    if k == 1980:
        data['time'].append(1985)

for k in range(1991, end_year + 1):
    data['time'].append(k)

with open('milanuncios.json', 'w+') as file:
    file.write(json.dumps(data))

