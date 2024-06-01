from base64 import b64encode
from os.path import dirname, join as path_join
from json import dump as json_dump
import unittest

from PIL import Image, ImageDraw
import requests

from tesseract import image_to_bboxes, image_to_text


api_base_url = "http://localhost:8000/api"
image_name = "1.jpg"
tester_dir = dirname(__file__)


def load_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = b64encode(image_file.read()).decode("utf-8")
    return encoded_string


class TestOCRModule(unittest.TestCase):
    def setUp(self):
        self.api_base_url = api_base_url
        self.image_file_path = path_join(tester_dir, image_name)
        self.not_image_file_path = path_join(tester_dir, "1.txt")
        self.json_output_path = path_join(tester_dir, "examples.json")

        self.api_specs = {
            '/api/get-text': [],
            '/api/get-bboxes': [],
        }
    
    def update_api_specs(self, endpoint, request, response):
        self.api_specs[endpoint].append({
            'request': request,
            'response': response,
        })
        
        with open(self.json_output_path, 'w') as f:
            json_dump(self.api_specs, f, indent=4)

    def debug_draw_bboxes_on_image(self, image_path, bboxes, output_path):
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        
        for bbox in bboxes:
            x_min = bbox['x_min']
            y_min = bbox['y_min']
            x_max = bbox['x_max']
            y_max = bbox['y_max']
            
            draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=2)
        
        image.save(output_path)

    def get_text(self):
        url = f"{self.api_base_url}/get-text"
        base64_image = load_image_as_base64(self.image_file_path)
        request_body = {
            "base64_image": base64_image,
        }

        response = requests.post(url, json=request_body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        response_data = response.json()

        self.assertEqual(response_data['success'], True)

        image = Image.open(self.image_file_path)
        expected_text = image_to_text(image)

        self.assertEqual(response_data['result']['text'], expected_text)

        request_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': {
                "base64_image": "A valid base64 encoded image.",
            },
        }
        response_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': response_data,
        }
        self.update_api_specs("/api/get-text", request_obj, response_obj)
    
    def get_text_invalid_base64_image(self):
        url = f"{self.api_base_url}/get-text"
        request_body = {
            "base64_image": "foo_bar",
        }

        response = requests.post(url, json=request_body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        response_data = response.json()

        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['error']['message'], "Invalid base64_image.")

        request_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': {
                "base64_image": "An invalid base64 encoded image.",
            },
        }
        response_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': response_data,
        }
        self.update_api_specs("/api/get-text", request_obj, response_obj)


        url = f"{self.api_base_url}/get-text"
        base64_image = load_image_as_base64(self.not_image_file_path)
        request_body = {
            "base64_image": base64_image,
        }

        response = requests.post(url, json=request_body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        response_data = response.json()

        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['error']['message'], "Invalid base64_image.")

        request_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': {
                "base64_image": "A non-image file encoded in base64.",
            },
        }
        response_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': response_data,
        }
        self.update_api_specs("/api/get-text", request_obj, response_obj)

    def get_bboxes(self):
        url = f"{self.api_base_url}/get-bboxes"
        base64_image = load_image_as_base64(self.image_file_path)

        bbox_types = ["word", "line", "paragraph", "block", "page"]

        for bbox_type in bbox_types:
            request_body = {
                "base64_image": base64_image,
                "bbox_type": bbox_type,
            }

            response = requests.post(url, json=request_body)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers["Content-Type"], "application/json")

            response_data = response.json()

            self.assertEqual(response_data['success'], True)

            response_bboxes = response_data['result']['bboxes']

            image = Image.open(self.image_file_path)
            expected_bboxes = image_to_bboxes(image, bbox_type)

            self.assertEqual(len(response_bboxes), len(expected_bboxes))
            for i in range(len(response_bboxes)):
                self.assertEqual(response_bboxes[i]['x_min'], expected_bboxes[i]['x_min'])
                self.assertEqual(response_bboxes[i]['y_min'], expected_bboxes[i]['y_min'])
                self.assertEqual(response_bboxes[i]['x_max'], expected_bboxes[i]['x_max'])
                self.assertEqual(response_bboxes[i]['y_max'], expected_bboxes[i]['y_max'])
            
            self.debug_draw_bboxes_on_image(self.image_file_path, response_bboxes, path_join(tester_dir, f"{bbox_type}-bboxes.png"))
        
        request_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': {
                "base64_image": "A valid base64 image.",
                "bbox_type": "word",
            },
        }
        response_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': response_data,
        }
        self.update_api_specs("/api/get-bboxes", request_obj, response_obj)

    def get_bboxes_invalid_base64_image(self):
        url = f"{self.api_base_url}/get-bboxes"
        request_body = {
            "base64_image": "foo_bar",
            "bbox_type": "word",
        }

        response = requests.post(url, json=request_body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        response_data = response.json()

        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['error']['message'], "Invalid base64_image.")

        request_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': {
                "base64_image": "An invalid base64 encoded image.",
                "bbox_type": "word",
            },
        }
        response_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': response_data,
        }
        self.update_api_specs("/api/get-bboxes", request_obj, response_obj)


        url = f"{self.api_base_url}/get-bboxes"
        base64_image = load_image_as_base64(self.not_image_file_path)
        request_body = {
            "base64_image": base64_image,
            "bbox_type": "word",
        }

        response = requests.post(url, json=request_body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        response_data = response.json()

        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['error']['message'], "Invalid base64_image.")

        request_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': {
                "base64_image": "A non-image file encoded in base64.",
                "bbox_type": "word",
            },
        }
        response_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': response_data,
        }
        self.update_api_specs("/api/get-bboxes", request_obj, response_obj)

    def get_bboxes_invalid_type(self):
        url = f"{self.api_base_url}/get-bboxes"
        base64_image = load_image_as_base64(self.image_file_path)
        request_body = {
            "base64_image": base64_image,
            "bbox_type": "foo",
        }

        response = requests.post(url, json=request_body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        response_data = response.json()

        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['error']['message'], "Invalid bbox_type.")

        request_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': {
                "base64_image": "A valid base64 encoded image.",
                "bbox_type": "foo",
            },
        }
        response_obj = {
            'headers': {
                'Content-Type': "application/json",
            },
            'body': response_data,
        }
        self.update_api_specs("/api/get-bboxes", request_obj, response_obj)

    def test__all(self):
        self.get_text()
        self.get_text_invalid_base64_image()
        self.get_bboxes()
        self.get_bboxes_invalid_base64_image()
        self.get_bboxes_invalid_type()

if __name__ == "__main__":
    unittest.main()
