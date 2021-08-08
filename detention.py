'''
爬出拘役天數
'''

import re
import cn2an

pattern_detention = re.compile(
    r'(?<=拘役)[壹貳叁肆伍陸柒捌玖拾貮兩佰仟]+(?=日)')

def find_detention(text: str) -> list:
    res = [cn2an.cn2an(match.group(0), 'strict').replace('貳', '二').replace('陸', '六') for match in pattern_detention.finditer(text)]
    if res:
        return max(res)
    return 0


if __name__ == '__main__':
    test_str = '方人毅服用酒類，不能安全駕駛動力交通工具而駕駛，處拘役伍拾日，如易科罰金，以新臺幣壹仟元折算壹日。'
    print(find_detention(test_str))
