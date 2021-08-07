'''
把字串內判決跟價錢有關的關鍵詞抓出來並轉成數字
'''

import re
import cn2an


pattern_money = re.compile(
    r'(?<=新臺幣)[壹一貳二叁三肆四伍五陸六柒七捌八玖九拾十貮二兩佰百千仟]+(?=元)')


if __name__ == '__main__':
    main_text = '''被告應給付原告新臺幣柒佰玖拾捌元，及自民國101 年3 月14日起至清償日止按週年利率百分之五計算之利息。
原告其餘之訴駁回。
本判決第1 項得假執行。但被告如於執行標的物拍定、變賣或物之交付前，以新臺幣柒佰玖拾捌元預供擔保，得免為假執行。
原告其餘假執行之聲請駁回。'''
    for match in pattern_money.finditer(main_text):
        print(cn2an.cn2an(match.group(0), 'smart'))
