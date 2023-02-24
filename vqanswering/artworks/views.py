from django.shortcuts import render, redirect

from .models import Artwork, Question_Answer
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .answer_generator import AnswerGenerator
from .import_datas import import_datas
import json


def home_view(request):
    obj = Artwork.objects.all()
    context = {'artwork': obj}

    # to delete an Artwork
    # delete_artwork1 = Artwork.objects.filter(image="https://upload.wikimedia.org/wikipedia/commons/c/cd/Dauerausstellung_360GRAZ_-_Euphrosina_Scholastica_Dann_de_Wilfersdorf%2C_Baronissa_A._Maswanau%2C_1636.jpg").delete()
    # delete_artwork2 = Artwork.objects.filter(image="https://upload.wikimedia.org/wikipedia/commons/1/16/Dauerausstellung_360GRAZ_-_Ionas_Liber_Baro_a_Wilfersdorf%2C_1635.jpg").delete()
    # delete_artwork3 = Artwork.objects.filter(image="https://upload.wikimedia.org/wikipedia/commons/a/a2/Dauerausstellung_360GRAZ_-_Maria_Anna_Remschmidin_aus_Graz%2C_die_Gattin_des_Maurermeisters_Witalm_auf_einem_Gem%C3%A4lde_von_Josef_Schlanderer_um_1810.jpg").delete()
    # delete_artwork4 = Artwork.objects.filter(image="https://portal-os.si/wp-content/uploads/sites/15/2019/09/KOLIZEJ-01-255x300.jpg").delete()

    # to add an Artwork
    # json_file = json.load(open('./static/assets/json/rehineritpedia.json', 'rb'))
    # import_datas(json_file, Artwork)

    return render(request, "index.html", context)


def gallery_view(request):
    obj = Artwork.objects.all().order_by('year')
    context = {'artwork': obj}

    return render(request, "gallery.html", context)


class ArtworkDetails(View):
    art = "momentaneo"

    def get(self, request):
        obj = Question_Answer.objects.all()
        questions = []
        for element in obj:
            if element.title == self.art.title:
                questions.append(element)

        context = {'artwork': self.art, 'question': questions, 'chat_link': self.art.link + '/chat/'}
        return render(request, "gallery-details.html", context)


class Artworkchat(View):
    art = "tmp"

    def post(self, request):
        context = {'artwork': self.art}
        return render(request, "artwork-chat.html", context)

    def get(self, request):
        context = {'artwork': self.art}
        return render(request, "artwork-chat.html", context)


@csrf_exempt
def handle_chat_question(request):
    img_url = request.POST["img"]
    question = request.POST["question"]
    artwork = Artwork.objects.get(image=img_url)
    v_desc = artwork.visual_description
    c_desc = artwork.contextual_description
    title = artwork.title
    year = " this painting was depicted in " + str(artwork.year)
    text_info = c_desc + year + ' ' + v_desc
    img_feats = img_url
    answer = AnswerGenerator().produce_answer(question, title, str(artwork.year), text_info, img_feats)

    return JsonResponse({'answer': answer})


def chat_view(request):
    return render(request, "chat.html")
