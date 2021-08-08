import json
import os
import sys
import logging

from glob import glob
from pathlib import Path
from time import time

import pandas as pd
from tqdm import tqdm

import detention
import keyword_counter
import money

# import Get_Address


if __name__ == '__main__':
    logging.basicConfig(filename='main.log', level=logging.DEBUG)
    start = time()
    columns = [
        'filename',
        'money',
        'detention',
        # 'address'
    ]
    columns += list(keyword_counter.get_keys())

    csv_data = dict((column, []) for column in columns)
    pattern = str(Path(__file__).parent.joinpath('input').joinpath('*.json'))
    for filename in tqdm(glob(pattern)):
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)

        try:
            text = data['mainText'] + data['opinion']

            csv_data['filename'].append(os.path.basename(filename))
            csv_data['money'].append(money.find_money(text))
            csv_data['detention'].append(detention.find_detention(text))
            # csv_data['address'].append(Get_Address.GetAddress(text))

            res = keyword_counter.count_words(text)
            for key in keyword_counter.get_keys():
                csv_data[key].append(res[key])
        except:
            logging.error(data, exc_info=True)
            print("Error:", filename, file=sys.stderr)


    # print(csv_data)
    pd.DataFrame(data=csv_data).to_csv('result.csv', index=True, encoding='utf-8')
    print(f"Time used: {time() - start}", file=sys.stderr)
