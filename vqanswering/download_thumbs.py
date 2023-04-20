import errno
import os
import json
import requests
from io import BytesIO
from PIL import Image

here = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.abspath(os.path.join(here, os.pardir))
# print('parent: ', parent)
# print('here: ', here)
thumbs_path = os.path.join(here, 'static/assets/img/thumbs')
full_path = os.path.join(here, 'static/assets/img/full')
if not os.path.exists(thumbs_path):
    os.makedirs(thumbs_path)
if not os.path.exists(full_path):
    os.makedirs(full_path)
headers = {
  # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
  'User-Agent': 'FACEFIT (fitface.unifi@gmail.com)'
}
Image.MAX_IMAGE_PIXELS = None
def thumbnails(image_url):
    try:


        file_name = image_url.split("/")[-1]
        print('trying... ', file_name)
        if file_name in os.listdir(thumbs_path):
            print('file_name: ', file_name)
            return file_name
        response = requests.get(image_url + "?raw=true", headers=headers)
        t_width = 300
        i_width = 1000
        print('response: ', response)
        image = Image.open(BytesIO(response.content))
        print('image: ', image)
        t_delta = float(t_width / image.size[0])
        t_size = int((float(image.size[1]) * t_delta))
        i_delta = float(i_width / image.size[0])
        i_size = int((float(image.size[1]) * i_delta))
        print('size: ', t_size)
        t_resized = image.resize((t_width, t_size), Image.LANCZOS)
        i_resized = image.resize((i_width, i_size), Image.LANCZOS)
        print('resized: ', t_resized)
         # + '_thumbnail.jpg'
        print('file_name: ', file_name)
        thumb = os.path.join(thumbs_path + '/' + file_name)
        full = os.path.join(full_path + '/' + file_name)
        print('thumb: ', thumb, 'full: ', full)
        i_resized.save(full)
        t_resized.save(thumb)
        print('file_name: ', file_name)
        return file_name
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
def create_thumb(image_url):
    # if normal_image.find('wikimedia') != -1:
    #     style = normal_image.split("/")[4]
    #
    #     if style == "en":
    #         thumb_image = normal_image.replace('/en/', '/en/thumb/') + "/300px-"
    #     else:
    #         thumb_image = normal_image.replace('/commons/', '/commons/thumb/') + "/300px-"
    #     new_part = normal_image.split("/")[-1]
    #     thumb_url = thumb_image + new_part
    #     thumb_image = thumb_url
    # else:
    thumb_path = "/static/assets/img/thumbs/" + thumbnails(image_url)

    return thumb_path


# Load the JSON file containing the image URLs
with open('./static/assets/json/artpedia.json') as f:
    data = json.load(f)

# Create the "thumbs" folder if it doesn't exist
if not os.path.exists('thumbs'):
    os.makedirs('thumbs')

# Loop through the image URLs and download the thumbnails
for image in data:
    web_url = data[image]['img_url']
    thumb_path = create_thumb(web_url)
    # response = requests.get(data[image]['img_url'])
    thumb_name = os.path.join('thumbs', thumb_path.split('/')[-1])
    # print(thumb_path, thumb_name)
    # with open(thumb_path, 'wb') as f:
    #     f.write(response.content)
