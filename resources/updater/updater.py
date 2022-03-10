import os
import sys
import requests
import platform

from bs4 import BeautifulSoup

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(os.path.abspath(__file__))

def tree_download(link: str, tag: str, dir: str, filter_dirs: list):
    link = requests.get(link)
    soup = BeautifulSoup(link.text, 'html.parser')
    items = soup.find_all("div", {"class": tag})
    items_txt = [x.getText().replace('\n', ' ').split()[0] for x in items]
    items_url = ['https://github.com' + 
                x.find("a").attrs['href'] for x in items]
    items_typ = [x.find("svg").attrs['aria-label'] for x in items]

    for item, url, type in zip(items_txt, items_url, items_typ):
        if item not in filter_dirs:
            if type == "Directory":
                item_dir = os.path.join(dir, item)
                if not os.path.isdir(item_dir):
                    os.makedirs(item_dir)
                tree_download(url, tag, item_dir, filter_dirs)
            else:
                link = url.replace('/blob', '').replace('https://github.com', 
                    'https://raw.githubusercontent.com')
                with open(os.path.join(dir,item), "wb") as f:
                    print("Downloading %s" % item)
                    response = requests.get(link, stream=True)
                    total_length = response.headers.get('content-length')

                    if total_length is None: # no content length header
                        f.write(response.content)
                    else:
                        dl = 0
                        total_length = int(total_length)
                        disp_bars = 25
                        for data in response.iter_content(chunk_size=int(total_length/disp_bars)):
                            dl += len(data)
                            f.write(data)
                            done = int(disp_bars * dl / total_length)
                            if done > disp_bars:
                                done = disp_bars
                            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (disp_bars-done)) )    
                            sys.stdout.flush()

                    print('\n')
            
def main():
    url = 'https://github.com/Azaz3l0z/car_project/'+\
          'tree/{sys}/resources'.format(sys=platform.system().lower())
    tag = 'Box-row Box-row--focus-gray py-2 d-flex position-relative '+\
          'js-navigation-item'
    tree_download(url, tag, os.path.dirname(application_path),
        ['updater'])

if __name__ == "__main__":
    main()