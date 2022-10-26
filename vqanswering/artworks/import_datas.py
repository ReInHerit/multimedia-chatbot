import math


def first_n_digits(num, n):
    return num // 10 ** (int(math.log(num, 10)) - n + 1)


def create_thumb(normal_image):
    style = normal_image.split("/")[4]
    if style == "en":
        thumb_image = normal_image.replace('/en/', '/en/thumb/') + "/300px-"
    else:
        thumb_image = normal_image.replace('/commons/', '/commons/thumb/') + "/300px-"
    new_part = normal_image.split("/")[7]
    thumb_image = thumb_image + new_part
    return thumb_image


def create_link(to_do_link):
    link = str(to_do_link)
    new_link = link.replace(" ", "-")
    return new_link


def import_datas(json_data, data):
    for article_id in json_data:
        century = first_n_digits(json_data[article_id]['year'], 2) * 100
        data.create(title=json_data[article_id]['title'],
                    image=json_data[article_id]['img_url'],
                    thumb_image=create_thumb(json_data[article_id]['img_url']),
                    year=json_data[article_id]['year'],
                    visual_description=json_data[article_id]['visual_sentences'],
                    contextual_description=json_data[article_id]['contextual_sentences'],
                    century=century,
                    link=create_link(json_data[article_id]['title']))


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
