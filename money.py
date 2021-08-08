'''
把字串內判決跟價錢有關的關鍵詞抓出來並轉成數字
'''

import re
import cn2an


pattern_money = re.compile(
    r'(?<=新臺幣)[壹貳叁肆伍陸柒捌玖拾貮兩佰仟萬億]+(?=元(?!折算))')

def find_money(text: str) -> int:
    res = [cn2an.cn2an(match.group(0).replace('萬', '万').replace('億', '亿'), 'strict') for match in pattern_money.finditer(text)]
    if res:
        return max(res)
    return 0


if __name__ == '__main__':
    '''test'''

    test_strings = ['''被告應給付原告新臺幣柒佰玖拾捌萬元，及自民國101 年3 月14日起至清償日止按週年利率百分之五計算之利息。
原告其餘之訴駁回。
本判決第1 項得假執行。但被告如於執行標的物拍定、變賣或物之交付前，以新臺幣柒佰玖拾捌元預供擔保，得免為假執行。
原告其餘假執行之聲請駁回。''',
'方人毅服用酒類，不能安全駕駛動力交通工具而駕駛，處拘役伍拾日，如易科罰金，以新臺幣壹仟元折算壹日。']
    for s in test_strings:
        print(find_money(s))
