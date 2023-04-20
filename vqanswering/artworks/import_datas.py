import math
import urllib
from urllib.parse import urlencode

def create_link(to_do_link):
    link = str(to_do_link)
    new_link = link.replace(" ", "-")
    return new_link


def import_datas(json_data, data):
    for article_id in json_data:
        file_name = urllib.parse.quote(json_data[article_id]['img_url'].split("/")[-1], safe="")
        century = (json_data[article_id]['year'] // 10 ** (int(math.log(json_data[article_id]['year'], 10)) - 1)) * 100
        data.objects.create(title=json_data[article_id]['title'],
                            image="/static/assets/img/full/" + file_name,  # json_data[article_id]['img_url'],
                            thumb_image="/static/assets/img/thumbs/" + file_name,  # create_thumb(json_data[article_id]['img_url']),
                            year=json_data[article_id]['year'],
                            visual_description=json_data[article_id]['visual_sentences'],
                            contextual_description=json_data[article_id]['contextual_sentences'],
                            century=century,
                            link=create_link(json_data[article_id]['title']))


