'''
「犯公然侮辱罪，處拘役xx日」
「犯公然侮辱罪，處罰金新台幣xx元」
「犯公然侮辱罪，累犯，處拘役xx日」
「犯公然侮辱罪，累犯，處罰金新台幣xx元」
「犯公然侮辱罪，科罰金新台幣xx元」
'''
import re
import cn2an



pattern = re.compile(
    r'犯公然侮辱罪，(?P<recidivism>累犯，)?[處科](拘役(?P<detention>[壹貳叁肆伍陸柒捌玖拾貮兩佰仟]+)日|(罰金新臺幣(?P<money>[壹貳叁肆伍陸柒捌玖拾貮兩佰仟萬億]+)元))'
)


def get_crime_data(text: str) -> dict:
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        return None
    data = matches[0].groupdict()
    data['recidivism'] = 0 if data['recidivism'] is None else 1
    for key in ['detention', 'money']:
        data[key] = 0 if data[key] is None else cn2an.cn2an(_cn2an_preprocess(data[key]), 'strict')
    data['detention_and_money'] = data['detention'] * 1000 + data['money']
    return data


def _cn2an_preprocess(text: str) -> str:
    return text.replace('萬', '万').replace('億', '亿').replace('貳', '二').replace('陸', '六')


if __name__ == '__main__':
    # test_str = '乙○○犯公然侮辱罪，處拘役肆拾日，如易科罰金，以新臺幣壹仟元折算壹日。'
    # test_str = "李昕樺犯公然侮辱罪，處罰金新臺幣貳仟元，如易服勞役，以新臺幣壹仟元折算壹日；又犯毀損他人物品罪，處罰金新臺幣貳仟元，如易服勞役，以新臺幣壹仟元折算壹日。應執行罰金新臺幣參仟元，如易服勞役，以新臺幣壹仟元折算壹日。\n歐守睿犯公然侮辱罪，共貳罪，各處罰金新臺幣貳仟元，如易服勞役，均以新臺幣壹仟元折算壹日；又犯毀損他人物品罪，處罰金新臺幣貳仟元，如易服勞役，以新臺幣壹仟元折算壹日。應執行罰金新臺幣伍仟元，如易服勞役，以新臺幣壹仟元折算壹日。"
    test_str = "楊翔渝犯公然侮辱罪，科罰金新臺幣伍仟元，如易服勞役，以新臺幣壹仟元折算壹日。"
    print(get_crime_data(test_str))
