### Nothing much here -_-
from flask import Flask, jsonify, request
from PIL import Image, ImageDraw
import requests
import pytesseract
from base64 import b64decode, b64encode
from io import BytesIO 

app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def decode_base64_image(base64_image):
    image_data = b64decode(base64_image)
    return Image.open(BytesIO(image_data))

def image_to_text(image):
    try: 
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(1,e)
        return f"{e}"

@app.route('/api/get-text', methods=['POST'])
def get_text():
    try: 
        data = request.get_json()
        image_data = data['base64_image'] 
        image = decode_base64_image(image_data)  
        text = pytesseract.image_to_string(image)
        return jsonify({'success': True, "result":{"text": text}}), 200
    except Exception as e:
        return jsonify({'success': False, "error":{"message": f"Invalid base64_image."}}), 400


def image_to_bboxes(image, bbox_type):
    # You are to implement this in your server code.
    try:
        if bbox_type == 'word':
            boxes = pytesseract.image_to_boxes(image)
            bboxes = []
            for b in boxes.splitlines():
                b = b.split(' ')
                bbox = {
                    'x_min': int(b[1]),
                    'y_min': int(b[2]),
                    'x_max': int(b[3]),
                    'y_max': int(b[4])
                }
                bboxes.append(bbox)
            return bboxes
        elif bbox_type in ['line', 'paragraph', 'block', 'page']:
        # Use 'image_to_data' for more detailed bounding boxes for other types
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            bboxes = []
            for i in range(len(data['level'])):
                if bbox_type == 'line' and data['level'][i] == 2:
                    bboxes.append({
                        'x_min': data['left'][i],
                        'y_min': data['top'][i],
                        'x_max': data['left'][i] + data['width'][i],
                        'y_max': data['top'][i] + data['height'][i]
                    })
                elif bbox_type == 'paragraph' and data['level'][i] == 3:
                    bboxes.append({
                        'x_min': data['left'][i],
                        'y_min': data['top'][i],
                        'x_max': data['left'][i] + data['width'][i],
                        'y_max': data['top'][i] + data['height'][i]
                    })
                elif bbox_type == 'block' and data['level'][i] == 1:
                    bboxes.append({
                        'x_min': data['left'][i],
                        'y_min': data['top'][i],
                        'x_max': data['left'][i] + data['width'][i],
                        'y_max': data['top'][i] + data['height'][i]
                    })
                elif bbox_type == 'page' and data['level'][i] == 0:
                    bboxes.append({
                        'x_min': data['left'][i],
                        'y_min': data['top'][i],
                        'x_max': data['left'][i] + data['width'][i],
                        'y_max': data['top'][i] + data['height'][i]
                    })
                else:
                    pass
                
            return bboxes
    except Exception as e:
        print(4,e)
        return jsonify({'success': False, "error":{"message": f"Invalid base64_image."}}), 400


@app.route('/api/get-bboxes', methods=['POST'])
def get_bboxes():
    try: 
        ''' request_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': {
                "base64_image": "A valid base64 image.",
                "bbox_type": "word",
            },
        }
        response_obj = {
        'headers': { 'Content-Type': "application/json",}, 
        'body': response_data, } 
        
        response_data['success'], True)
        response_bboxes = response_data['result']['bboxes']

        '''

        data = request.get_json()
        image_data = data['base64_image']
        bbox_type = data['bbox_type']
        print(1, bbox_type)
        image = decode_base64_image(image_data)

        if bbox_type == 'word':
            # print(2)
            boxes = pytesseract.image_to_boxes(image)
            bboxes = []
            # print(3)
            for b in boxes.splitlines():
                
                b = b.split(' ')
                bbox = {
                    'x_min': int(b[1]),
                    'y_min': int(b[2]),
                    'x_max': int(b[3]),
                    'y_max': int(b[4])
                }
                bboxes.append(bbox)
            # print(4)
            
            # print(len(bboxes))
            # print(5)
            return jsonify({"success":True,"result":{"bboxes":bboxes}}), 200
        
        elif bbox_type in ['line', 'paragraph', 'block', 'page']:
            print(7, bbox_type)
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            bboxes = []
            for i in range(len(data['level'])):
                # print(i,data['level'][i])
                if bbox_type == 'line' and data['level'][i] == 2:
                    bboxes.append({
                        'x_min': data['left'][i],
                        'y_min': data['top'][i],
                        'x_max': data['left'][i] + data['width'][i],
                        'y_max': data['top'][i] + data['height'][i]
                    })
                elif bbox_type == 'paragraph' and data['level'][i] == 3:
                    bboxes.append({
                        'x_min': data['left'][i],
                        'y_min': data['top'][i],
                        'x_max': data['left'][i] + data['width'][i],
                        'y_max': data['top'][i] + data['height'][i]
                    })
                elif bbox_type == 'block' and data['level'][i] == 1:
                    bboxes.append({
                        'x_min': data['left'][i],
                        'y_min': data['top'][i],
                        'x_max': data['left'][i] + data['width'][i],
                        'y_max': data['top'][i] + data['height'][i]
                    })
                elif bbox_type == 'page' and data['level'][i] == 0:
                    bboxes.append({
                        'x_min': data['left'][i],
                        'y_min': data['top'][i],
                        'x_max': data['left'][i] + data['width'][i],
                        'y_max': data['top'][i] + data['height'][i]
                    })
                else:
                    pass
            print(9,bboxes)

            return jsonify({'success': True, "result":{"bboxes": bboxes}}), 200
        
        else:
            print(8)
            return jsonify({'success': False, "error":{"message": f"Invalid bbox_type."}}), 400
        
    except Exception as e:
        print(6,e)
        return jsonify({'success': False, "error":{"message": f"Invalid base64_image."}}), 400






if __name__ == '__main__':
    app.run(port=8000)