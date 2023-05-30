import errno
import os
import json
import requests
from io import BytesIO
from PIL import Image

here = os.path.dirname(os.path.realpath(__file__))
parent = os.path.abspath(os.path.join(here, os.pardir))
thumbs_path = os.path.join(parent, 'static/assets/img/thumbs')
full_path = os.path.join(parent, 'static/assets/img/full')
if not os.path.exists(thumbs_path):
    os.makedirs(thumbs_path)
if not os.path.exists(full_path):
    os.makedirs(full_path)
headers = {
  'User-Agent': 'FACEFIT (fitface.unifi@gmail.com)'
}
Image.MAX_IMAGE_PIXELS = None


def create_thumb(image_url, file_name):
    try:
        print('trying... ', file_name)
        if file_name in os.listdir(thumbs_path):
            return file_name
        response = requests.get(image_url + "?raw=true", headers=headers)
        t_width = 300
        i_width = 1000

        image = Image.open(BytesIO(response.content))
        print('image: ', image)

        if image.mode == 'RGBA':
            print("Image has an alpha channel, so convert it to RGB")
            image = image.convert('RGB')

        t_delta = float(t_width / image.size[0])
        t_size = int((float(image.size[1]) * t_delta))
        i_delta = float(i_width / image.size[0])
        i_size = int((float(image.size[1]) * i_delta))

        t_resized = image.resize((t_width, t_size), Image.LANCZOS)
        i_resized = image.resize((i_width, i_size), Image.LANCZOS)

        # file_name
        thumb = os.path.join(thumbs_path, file_name)
        full = os.path.join(full_path, file_name)
        i_resized.save(full)
        t_resized.save(thumb)
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
    thumb_path = "/static/assets/img/thumbs/" + file_name

    return thumb_path

