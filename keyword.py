'''
統計關鍵詞
'''

import re

if __name__ == '__main__':
    file = 'testfile.txt'
    main_text = 'testmaintext.txt'
    with open(file, 'r') as f:
        keyword_list = f.read().split()
    pattern = re.compile('|'.join(keyword_list))

    dic = {}

    with open(main_text, 'r') as f:
        for match in pattern.finditer(f.read()):
            keyword = match.group(0)
            dic.setdefault(keyword, 0)
            dic[keyword] += 1

    print(dic)
