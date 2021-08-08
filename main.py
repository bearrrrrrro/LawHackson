import json
import os

from pathlib import Path
from glob import glob

import pandas as pd

import keyword_counter
import money
import detention
# import Get_Address


if __name__ == '__main__':
    columns = [
        'filename',
        'money',
        'detention',
        # 'address'
    ]
    columns += list(keyword_counter.get_keys())

    csv_data = dict((column, []) for column in columns)
    pattern = str(Path(__file__).parent.joinpath('input').joinpath('*.json'))
    for filename in glob(pattern):
        with open(filename, 'r') as f:
            data = json.load(f)

        text = data['mainText'] + data['opinion']

        csv_data['filename'].append(os.path.basename(filename))
        csv_data['money'].append(money.find_money(text))
        csv_data['detention'].append(detention.find_detention(text))
        # csv_data['address'].append(Get_Address.GetAddress(text))

        res = keyword_counter.count_words(text)
        for key in keyword_counter.get_keys():
            csv_data[key].append(res[key])

    # print(csv_data)
    pd.DataFrame(data=csv_data).to_csv('result.csv', index=True)
