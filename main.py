import json
import logging
import os
import sys
from multiprocessing import Pool, cpu_count
from pathlib import Path
from time import time
import re

import pandas as pd
from tqdm import tqdm

import crime
import keyword_counter
import location
import judge
import preprocess


def _run(index, judge_path):
    if not judge_path.is_dir():
        return
    error_count = 0
    csv_data = []
    pbar = tqdm(list(judge_path.iterdir()), position=index)
    pbar.set_description(judge_path.name)
    for filename in pbar:
        if filename.suffix != '.json':
            continue
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
        # 過濾罪名
        try:
            crime_data = crime.get_crime_data(data['mainText'])
            if crime_data is None:
                continue
            text = preprocess.text_preprocess(data['judgement'] + data['opinion'])
            row_data = {
                'filename': os.path.basename(filename),
                'is_internet': 1 if location.is_internet(text) else 0,
                'reason': data['reason']
            }

            res = keyword_counter.count_words(text)
            jud = judge.get_judge(data['mainText'])
            row_data = dict(row_data, **jud, **crime_data, **res)
            csv_data.append(row_data)
        except:
            logging.error(data, exc_info=True)
            error_count += 1

    result = pd.DataFrame.from_records(data=csv_data)
    result['來源'] = judge_path.name
    print(f"Error: {error_count}", file=sys.stderr)
    try:
        result = result[result['detention_and_money'] > 0]

        # reorder columns
        cols = result.columns.tolist()
        cols = cols[:1] + cols[-1:] + cols[1:-1]
        result = result[cols]
        return result
    except:
        return


if __name__ == '__main__':
    if os.path.isfile('result.csv'):
        print("請先把舊的結果移除", file=sys.stderr)
        exit(-1)
    logging.basicConfig(filename='main.log', level=logging.DEBUG)
    start_time = time()

    with Pool(cpu_count()) as pool:
        args = list(enumerate(Path(__file__).parent.joinpath('input').iterdir()))
        pd.concat(df for df  in pool.starmap(_run, args) if df is not None and not df.empty).to_csv('result.csv', index=False, encoding='utf-8')
    print(f'Total time used: {(time() - start_time):.2f} sec', file=sys.stderr)
