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


def _output_money(df: pd.DataFrame, filename: str) -> pd.DataFrame:
    result = df.drop(columns=['detention'])
    return result[result['money'] > 0]


def _output_detention(df: pd.DataFrame, filename: str) -> pd.DataFrame:
    result = df.drop(columns=['money'])
    return result[result['detention'] > 0]


def _run(index, judge_path):
    error_count = 0
    csv_data = []
    pbar = tqdm(list(judge_path.iterdir()), position=index)
    pbar.set_description(judge_path.name)
    for filename in pbar:
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
            error_count += 1

    result = pd.DataFrame.from_records(data=csv_data)
    result['source'] = judge_path.name
    money_df = _output_money(result, judge_path.name)
    detention_df = _output_detention(result, judge_path.name)
    print(f"Error: {error_count}", file=sys.stderr)
    return money_df, detention_df


if __name__ == '__main__':
    if os.path.isfile('money.csv') or os.path.isfile('detention.csv'):
        print("Please remove the previous results first.", file=sys.stderr)
        exit(-1)
    logging.basicConfig(filename='main.log', level=logging.DEBUG)
    start_time = time()

    with Pool(cpu_count()) as pool:
        args = list(enumerate(Path(__file__).parent.joinpath('input').iterdir()))
        money_concat = []
        detention_concat = []
        for money_df, detention_df in pool.starmap(_run, args):
            money_concat.append(money_df)
            detention_concat.append(detention_df)
        pd.concat(money_concat).to_csv('money.csv', index=False,  encoding='utf-8')
        pd.concat(detention_concat).to_csv('detention.csv', index=False,  encoding='utf-8')
    print(f'Total time used: {(time() - start_time):.2f} sec', file=sys.stderr)
