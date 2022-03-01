import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas

def main(*args):
    for k in args:
        print(k)

