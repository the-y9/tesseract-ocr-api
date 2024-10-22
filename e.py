import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

try:
    img = Image.open('1.jpg')
    boxes = pytesseract.image_to_boxes(img)
    # print(boxes[:100])
    '''<character> <left> <bottom> <right> <top> <page>'''

    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    print(data)
    '''dict_keys(['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text'])'''
    bbox_types = ["word", "line", "paragraph", "block", "page"]
    '''  word_num,line_num,par_num,block_num,page_num
        'x_min' 'y_min' 'x_max' 'y_max'
    '''

except Exception as e:
    print(e)