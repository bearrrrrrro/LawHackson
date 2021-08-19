'''
可以抓否定詞但慢很多
'''

import json
from pathlib import Path
import re

files = ['attitude.json', 'background.json', 'content.json', 'crime.json']

filepaths = [Path(__file__).parent.joinpath('data').joinpath(filename) for filename in files]
data = {}
for filepath in filepaths:
    with open(filepath, mode='r', encoding='utf-8') as jsonfile:
        data = dict(json.load(jsonfile), **data)

empty_dict = dict((key, 0) for key in data.keys())

reversed_data = {}
for key, value in data.items():
    for word in value:
        reversed_data[word] = key
neg = '|'.join('不 未 否'.split())
to_match = '|'.join(reversed_data.keys())
pattern = re.compile(f'(?<!{neg})({to_match})')




def get_keys():
    return empty_dict.keys()


def count_words(text: str) -> dict:
    dic = empty_dict.copy()
    for match in pattern.finditer(text):
        dic[reversed_data[match.group(0)]] = 1
    return dic


if __name__ == '__main__':
    haystack = '幹你娘勒我學他那種機掰個性，說那種機掰懶叫話幹你娘雞掰勒幹你娘勒你吃洨（閩南語，泛指精液）也沒有人要看你知道幹你娘幹你娘你連屁都不如嘛，你什麼洨'
    print(count_words(haystack))
