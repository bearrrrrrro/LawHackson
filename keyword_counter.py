'''
Improved keyword counter using AC-automata
'''

import ahocorasick
import json
from pathlib import Path
import re

files = ['attitude.json', 'background.json', 'content.json', 'crime.json']

filepaths = [Path(__file__).parent.joinpath('data').joinpath(filename) for filename in files]
data = {}
for filepath in filepaths:
    with open(filepath, mode='r', encoding='utf-8') as jsonfile:
        data = dict(json.load(jsonfile), **data)

automaton = ahocorasick.Automaton()
idx = 0
empty_dict = {}
for key, value in data.items():
    for word in value:
        automaton.add_word(word, (idx, word, key))
        empty_dict[key] = 0
        idx += 1

automaton.make_automaton()

neg = re.compile(r'(未|否|不|未能)$')


def get_keys():
    return empty_dict.keys()


def count_words(text: str) -> dict:
    dic = empty_dict.copy()
    for end_index, (_, original_value, keyword) in automaton.iter(text):
        start_index = end_index - len(original_value) + 1
        if not neg.match(text[max(start_index - 2, 0): start_index]):
            dic[keyword] = 1
    return dic


if __name__ == '__main__':
    haystack = '不公然侮辱罪幹你娘勒我學他那種機掰個性，說那種機掰懶叫話幹你娘雞掰勒幹你娘勒你吃洨（閩南語，泛指精液）也沒有人要看你知道幹你娘幹你娘你連屁都不如嘛，你什麼洨'
    print(count_words(haystack))
