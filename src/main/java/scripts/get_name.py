import os
import sys

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

    test_file = 'file.txt'
    scripts_path: str = os.path.dirname(os.path.abspath(__file__))
    files_path: str = os.path.join(os.path.dirname(scripts_path), 'files')
    json_path: str = os.path.join(files_path, f'{webpage}.json')

    for file in os.listdir(scripts_path):
        if (webpage in file) and os.path.isfile((json_path)):
            frame = globals()[webpage].read_json(json_path)
            name = globals()[webpage].create_url(frame, trademark, model, yearstart, yearend, change, km)[1]
            print(name)

    
if __name__ == "__main__":
    main(*sys.argv[1:])

    

