import re


pattern = re.compile(r'[\r\n ]')


def text_preprocess(text: str) -> str:
    return pattern.sub('', text)


if __name__ == '__main__':
    text = 'abc \rdef \n  g'
    print(text_preprocess(text))
