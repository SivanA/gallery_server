from flask import Flask, request
from flask_cors import CORS, cross_origin
import requests
import json
import random

PICSUM_URL = "https://picsum.photos/v2/list?page=1&limit=100"
IMAGE_URL_TEMPLATE = "https://picsum.photos/id/{0}/1366/768"


client_ip_to_images = {}


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/get_images')
@cross_origin()
def get_images():
    client_ip = request.remote_addr
    image_pool = client_ip_to_images.get(client_ip, [])
    if not image_pool:
        image_pool = fetch_images()
        client_ip_to_images[client_ip] = image_pool

    pool_size = len(image_pool)
    selected_images = []
    for _ in range(5):
        selected_index = random.randint(0, pool_size - 1)
        pool_size -= 1

        selected_image = image_pool[selected_index]
        image_data = {
            'url': IMAGE_URL_TEMPLATE.format(selected_image['id']),
            'author': selected_image['author']
        }

        selected_images.append(image_data)
        image_pool.pop(selected_index)

    return json.dumps(selected_images)


def fetch_images():
    response = requests.get(PICSUM_URL)
    return json.loads(response.text)


if __name__ == '__main__':
    app.run()
