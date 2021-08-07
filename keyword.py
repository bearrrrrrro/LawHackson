'''
統計關鍵詞
'''

import re
from pathlib import Path

with open(Path(__name__).parent.joinpath('data').joinpath('attitude.txt')) as f:
    pattern_attitude = re.compile('|'.join(f.read().split()))

with open(Path(__name__).parent.joinpath('data').joinpath('background.txt')) as f:
    pattern_background = re.compile('|'.join(f.read().split()))

with open(Path(__name__).parent.joinpath('data').joinpath('content.txt')) as f:
    pattern_content = re.compile('|'.join(f.read().split()))


def _find_pattern(pattern, text) -> dict:
    dic = {}
    for match in pattern.finditer(text):
        keyword = match.group(0)
        dic.setdefault(keyword, 0)
        dic[keyword] += 1
    return dic

def find_attitude(text: str) -> dict:
    return _find_pattern(pattern_attitude, text)

def find_background(text: str) -> dict:
    return _find_pattern(pattern_background, text)

def find_content(text: str) -> dict:
    return _find_pattern(pattern_content, text)

if __name__ == '__main__':
    test_str = '幹你娘勒我學他那種機掰個性，說那種機掰懶叫話幹你娘雞掰勒幹你娘勒你吃洨（閩南語，泛指精液）也沒有人要看你知道幹你娘幹你娘你連屁都不如嘛，你什麼洨'
    print(find_attitude(test_str))
    print(find_background(test_str))
    print(find_content(test_str))
