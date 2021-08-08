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
import location

# import Get_Address


if __name__ == '__main__':
    logging.basicConfig(filename='main.log', level=logging.DEBUG)
    start = time()

    csv_data = []
    pattern = str(Path(__file__).parent.joinpath('input').joinpath('*.json'))
    error_count = 0
    for filename in tqdm(glob(pattern)):
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)

        try:
            text = data['mainText'] + data['opinion']
            row_data = {
                'filename': os.path.basename(filename),
                'money': money.find_money(text),
                'detention': detention.find_detention(text),
                'is_internet': location.is_internet(text),
                'crime': data['reason'],
                # 'address': Get_Address.GetAddress(text),
            }

            res = keyword_counter.count_words(text)
            row_data = dict(row_data, **res)
            if max(row_data["公然侮辱罪"], row_data["誹謗罪"]) > 0:
                csv_data.append(row_data)
        except:
            logging.error(data, exc_info=True)
            print("Error:", filename, file=sys.stderr)
            error_count += 1


    # print(csv_data)
    pd.DataFrame.from_records(data=csv_data).to_csv('result.csv', index=True, encoding='utf-8')
    print(f"Time used: {time() - start}, error: {error_count}", file=sys.stderr)
