import json
import logging
import os
import sys
from multiprocessing import Pool, cpu_count
from pathlib import Path
from time import time

import pandas as pd
from tqdm import tqdm

import detention
import keyword_counter
import location
import money


def _run(index, judge_path):
    error_count = 0
    csv_data = []
    pbar = tqdm(list(judge_path.iterdir()), position=index)
    pbar.set_description(judge_path.name)
    for filename in pbar:
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
        # 過濾罪名
        if data['reason'].find('公然侮辱') == -1:
            continue
        try:
            text = data['mainText'] + data['opinion']
            row_data = {
                'filename': os.path.basename(filename),
                'money': money.find_money(text),
                'detention': detention.find_detention(text),
                'is_internet': location.is_internet(text),
                'crime': data['reason']
                # 'address': Get_Address.GetAddress(text),
            }

            res = keyword_counter.count_words(text)
            row_data = dict(row_data, **res)
            csv_data.append(row_data)
        except:
            logging.error(data, exc_info=True)
            error_count += 1

    result = pd.DataFrame.from_records(data=csv_data)
    result['來源'] = judge_path.name
    result['拘役罰金加總'] = result['money'] + result['detention'] * 1000
    print(f"Error: {error_count}", file=sys.stderr)
    result = result[result['拘役罰金加總'] > 0]

    # reorder columns
    cols = result.columns.tolist()
    cols = cols[:1] + cols[-2:] + cols[1:-2]
    result = result[cols]
    return result


if __name__ == '__main__':
    if os.path.isfile('result.csv'):
        print("請先把舊的結果移除", file=sys.stderr)
        exit(-1)
    logging.basicConfig(filename='main.log', level=logging.DEBUG)
    start_time = time()

    with Pool(cpu_count()) as pool:
        args = list(enumerate(Path(__file__).parent.joinpath('input').iterdir()))
        pd.concat(pool.starmap(_run, args)).to_csv('result.csv', index=False, encoding='utf-8')
    print(f'Total time used: {(time() - start_time):.2f} sec', file=sys.stderr)
