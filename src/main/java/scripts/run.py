import os
import sys
import json
import pandas as pd

# To upload files to dropbox
from datetime import datetime
from azazelutils import dropbox_manager, info

# Scraping modules
import cochesnet
import milanuncios
import autoscout24


def main(webpage, trademark, model, yearstart, yearend, change, km):
    # We fix the Java's input variables
    webpage = webpage.replace("_", " ")
    trademark = trademark.replace("_", " ")
    model = model.replace("_", " ")
    yearstart = yearstart.replace("_", " ")
    yearend = yearend.replace("_", " ")
    change = change.replace("_", " ")
    km = km.replace("_", " ")

    # Upload data to dropbox
    token = 'KjuflX1NCx4AAAAAAAAAAZC_0k_v9uPmWOQgRbWiuT1vaQBL8f7Zmmr38MQgCvk0'
    now = datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
    name = f'{webpage}_{now}.json'

    data = json.dumps(info.get_data()).encode('utf-8')
    dbx = dropbox_manager.Manager(token)
    dbx.upload_dropbox('/logs_cochesnet', name, data)

    # We define useful strings and start scraping
    test_file = 'file.txt'
    scripts_path: str = os.path.dirname(os.path.abspath(__file__))
    files_path: str = os.path.join(os.path.dirname(scripts_path), 'files')
    json_path: str = os.path.join(files_path, f'{webpage}.json')

    for file in os.listdir(scripts_path):
        if (webpage == os.path.splitext(os.path.basename(file))[0]) and os.path.isfile((json_path)):
            scrape = globals()[webpage].main(json_path, trademark, model, yearstart, yearend, change, km)
            df = pd.DataFrame(scrape[0])
            df.to_csv(os.path.join(os.path.expanduser('~'), 'Desktop', scrape[1]), index=False)

    with open(os.path.join(scripts_path, test_file), 'w+') as file:
        file.write(scrape[2])

    
if __name__ == "__main__":
    main(*sys.argv[1:])

    

