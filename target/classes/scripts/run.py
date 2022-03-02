import os
import re
import sys
import json
import pandas as pd

import cochesnet
import milanuncios
import autoscout24

def main(webpage, trademark, model, yearstart, yearend, change, km):
    webpage = webpage.replace("_", " ")
    trademark = trademark.replace("_", " ")
    model = model.replace("_", " ")
    yearstart = yearstart.replace("_", " ")
    yearend = yearend.replace("_", " ")
    change = change.replace("_", " ")
    km = km.replace("_", " ")

    file_path: str = os.path.dirname(os.path.abspath(__file__))
    test_file = 'file.txt'
    json_path: str = os.path.join(os.path.dirname(file_path), 'files', f'{webpage}.json')


    for file in os.listdir(file_path):
        if (webpage in file) and os.path.isfile((json_path)):
            scrape = globals()[webpage].main(json_path, trademark, model, yearstart, yearend, change, km)
            df = pd.DataFrame(scrape[0])
            df.to_excel(os.path.join(os.path.expanduser('~'), 'Desktop', scrape[1]), index=False)

    with open(os.path.join(file_path, test_file), 'w+') as file:
        file.write(scrape[2])
    
if __name__ == "__main__":
    main(*sys.argv[1:])

    

