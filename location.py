'''
Improved keyword counter using AC-automata
'''

import ahocorasick
from pathlib import Path

data = {}
filepath = Path(__file__).parent.joinpath('data').joinpath('location.txt')

with open(filepath, 'r', encoding='utf-8') as f:
    strings = f.read().split()

automaton = ahocorasick.Automaton()
for word in strings:
    automaton.add_word(word, word)

automaton.make_automaton()


def is_internet(text: str) -> dict:
    return bool(list(automaton.iter(text.lower())))


if __name__ == '__main__':
    haystack = '臉書幹你娘勒我學他那種機掰個性，說那種機掰懶叫話幹你娘雞掰勒幹你娘勒你吃洨（閩南語，泛指精液）也沒有人要看你知道幹你娘幹你娘你連屁都不如嘛，你什麼洨'
    print(is_internet(haystack))
