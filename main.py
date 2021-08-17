import json
import os
import sys
import logging

from pathlib import Path
from time import time

import pandas as pd
from tqdm import tqdm

import detention
import keyword_counter
import money
import location

# import Get_Address


def _output_money(df: pd.DataFrame, filename: str) -> None:
    result = df.drop(columns=['detention'])
    result[result['money'] > 0].to_csv(
        f'{filename}_with_money.csv', index=True, encoding='utf-8')


def _output_detention(df: pd.DataFrame, filename: str) -> None:
    result = df.drop(columns=['money'])
    result[result['detention'] > 0].to_csv(
        f'{filename}_with_detention.csv', index=True, encoding='utf-8')


def _run(judge_path):
    print(f'Processing {judge_path.name} ...', file=sys.stderr)
    error_count = 0
    csv_data = []
    for filename in tqdm(list(judge_path.iterdir())):
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
    _output_money(result, judge_path.name)
    _output_detention(result, judge_path.name)
    print(f"Time used: {time() - start}, error: {error_count}", file=sys.stderr)


if __name__ == '__main__':
    logging.basicConfig(filename='main.log', level=logging.DEBUG)
    start = time()

    for judge_path in Path(__file__).parent.joinpath('input').iterdir():
        _run(judge_path)
