import pandas as pd
import json
from glob import glob
filename = glob('*.json')[0]

def inputdata(filename):
    with open(filename, newline='',encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    print(data['mainText'])
    print(data['opinion'])
inputdata(filename)
