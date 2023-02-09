import math
from PIL import Image
import requests
from io import BytesIO
import os

here = os.path.dirname(os.path.realpath(__file__))
parent = os.path.abspath(os.path.join(here, os.pardir))
print('here', here, 'parent', parent)
thumbs_path = os.path.join(parent, 'static/assets/img/thumbs')
print(thumbs_path)


def first_n_digits(num, n):
    print('first', num, n)
    return num // 10 ** (int(math.log(num, 10)) - n + 1)


def thumbnails(image_url):
    try:
        response = requests.get(image_url)
        new_width = 300
        image = Image.open(BytesIO(response.content))
        concat = float(new_width / image.size[0])
        size = int((float(image.size[1]) * concat))
        print(image.width, image.height)
        resized = image.resize((new_width, size), Image.ANTIALIAS)
        if not os.path.exists(thumbs_path):
            os.makedirs(thumbs_path)
        file_name = image_url.split("/")[-1] + '_thumbnail.jpg'
        file_path = os.path.join(thumbs_path + '/' + file_name)
        resized.save(file_path)

        return file_name
    except IOError:
        print('error')
        pass


def uri_exists_stream(uri: str) -> bool:
    try:
        with requests.get(uri, stream=True) as response:
            try:
                response.raise_for_status()
                return True
            except requests.exceptions.HTTPError:
                return False
    except requests.exceptions.ConnectionError:
        return False


def create_thumb(normal_image):
    print('normal', normal_image)
    if normal_image.find('wikimedia') != -1:
        style = normal_image.split("/")[4]

        if style == "en":
            thumb_image = normal_image.replace('/en/', '/en/thumb/') + "/300px-"
        else:
            thumb_image = normal_image.replace('/commons/', '/commons/thumb/') + "/300px-"
        new_part = normal_image.split("/")[-1]
        thumb_url = thumb_image + new_part
        if uri_exists_stream(thumb_url):
            thumb_image = thumb_url
        else:
            thumb_image = "/static/assets/img/thumbs/" + thumbnails(normal_image)

    else:
        thumb_image = "/static/assets/img/thumbs/" + thumbnails(normal_image)
    print('np', thumb_image)
    print(normal_image.split('/'))

    print(thumb_image)
    return thumb_image


def create_link(to_do_link):
    link = str(to_do_link)
    new_link = link.replace(" ", "-")
    return new_link


def import_datas(json_data, data):
    for article_id in json_data:
        print('id', article_id)
        century = first_n_digits(json_data[article_id]['year'], 2) * 100
        data.objects.create(title=json_data[article_id]['title'],
                            image=json_data[article_id]['img_url'],
                            thumb_image=create_thumb(json_data[article_id]['img_url']),
                            year=json_data[article_id]['year'],
                            visual_description=json_data[article_id]['visual_sentences'],
                            contextual_description=json_data[article_id]['contextual_sentences'],
                            century=century,
                            link=create_link(json_data[article_id]['title']))
        print('fatto')


def import_autogen_qa(json_data, data):
    for article_id in json_data:
        data.create(title=json_data[article_id]['title'],
                    question=json_data[article_id]['question'],
                    answer=json_data[article_id]['answer'],
                    generation="auto generated",
                    sentence_type=json_data[article_id]['type'],
                    revised=False,
                    to_show=True,
                    dataset_version="second version")


def create_qa(json_data, data):
    for article_id in json_data:
        data.create(title=json_data[article_id]['title'],
                    question="In what year was it painted?",
                    answer=json_data[article_id]['year'],
                    generation="human generated",
                    sentence_type="contextual sentence")
        data.create(title=json_data[article_id]['title'],
                    question="What is the title of the work?",
                    answer=json_data[article_id]['title'],
                    generation="human generated",
                    sentence_type="contextual sentence")


def change_thumb(data):
    for element in data:
        new_link = element.thumb_image.replace("200", "300")
        element.thumb_image = new_link
        element.save()
