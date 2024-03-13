import cv2
import pytesseract
from io import BytesIO
from PIL import Image
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def process(file):
    if file.endswith('.pdf'):
        try:
            pages = convert_from_path(file,
                                      poppler_path=r'C:\\Program Files\\Release-21.03.0\\poppler-21.03.0\\Library\\bin')
            page = pages[0]
            file_name = 'temp.jpg'
            page.save(file_name)
            words = process_img(file_name)
        except:
            words = ''
    else:
        words = process_img(file)
    return words


def process_img(file):
    img = cv2.imread(file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    config = r'--oem 3 --psm 6'
    print(pytesseract.image_to_string(img, config=config, lang='rus+eng'))
    words = pytesseract.image_to_string(img, config=config, lang='rus+eng')
    data = pytesseract.image_to_data(img, config=config)

    # Перебираем данные про текстовые надписи
    for i, el in enumerate(data.splitlines()):
        if i == 0:
            continue
        el = el.split()
        try:
            # Создаем подписи на картинке
            x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
            cv2.rectangle(img, (x, y), (w + x, h + y), (0, 0, 255), 1)
            cv2.putText(img, el[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        except IndexError:
            print("Операция была пропущена")
    cv2.imshow('Result', img)
    cv2.waitKey(0)
    return words