import os
import textract
#pip i
extensions = [
    '.docx', '.doc', '.pptx',
]


def processor(path):
    extension = os.path.splitext(path)[1].lower()
    print(extension)
    if extension in extensions:
        text = textract.process(path, language='rus+eng').decode('UTF-8')
        return text
    return ''


print(processor('/Users/rustemkhakim/PycharmProjects/hack-purple/hackaton-cbr/тест.doc'))
