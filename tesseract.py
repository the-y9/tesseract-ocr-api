### Nothing much here -_-
from flask import Flask, jsonify, request
from PIL import Image
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
        return f"{e}"

@app.route('/api/get-text', methods=['POST'])
def get_text():
    try: 
        data = request.get_json()
        image_data = data['base64_image'] 
        image = decode_base64_image(image_data)  
        text = image_to_text(image)
        return jsonify({'success': True, "result":{"text": text}}), 200
    
    except Exception as e:
        return jsonify({'success': False, "error":{"message": f"Invalid base64_image."}}), 400


def image_to_bboxes(image, bbox_type):
    try:
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        level_mapping = {
            'word': 4,
            'line': 2,
            'paragraph': 3,
            'block': 1,
            'page': 0
        }
        
        if bbox_type in level_mapping:
            level = level_mapping[bbox_type]
            return [
                {
                    'x_min': data['left'][i],
                    'y_min': data['top'][i],
                    'x_max': data['left'][i] + data['width'][i],
                    'y_max': data['top'][i] + data['height'][i]
                }
                for i in range(len(data['level'])) if data['level'][i] == level
            ]
    except Exception as e:
        
        return jsonify({'success': False, "error":{"message": f"Invalid base64_image."}}), 400


@app.route('/api/get-bboxes', methods=['POST'])
def get_bboxes():
    try: 
        data = request.get_json()
        image_data = data['base64_image']
        bbox_type = data['bbox_type']
        
        image = decode_base64_image(image_data)

        if bbox_type in ["word", "line", "paragraph", "block", "page"]:
             
            bboxes = image_to_bboxes(image, bbox_type)
            return jsonify({'success': True, "result":{"bboxes": bboxes}}), 200
        
        else:
            
            return jsonify({'success': False, "error":{"message": f"Invalid bbox_type."}}), 400
        
    except Exception as e:
        
        return jsonify({'success': False, "error":{"message": f"Invalid base64_image."}}), 400

if __name__ == '__main__':
    app.run(port=8000)