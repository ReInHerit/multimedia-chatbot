from django.shortcuts import render, redirect

from .models import Artwork, Question_Answer
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .answer_generator import AnswerGenerator
from .import_datas import import_datas
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.conf import settings

ga_key = settings.GA_MEASUREMENT_ID


def home_view(request):
    obj = Artwork.objects.all()

    # TO DELETE A SINGLE ARTWORK
    # delete_artwork1 = Artwork.objects.filter(image="YOUR_IMAGE_URL").delete()

    # TO DELETE ALL ARTWORKS
    # obj.delete()

    # TO ADD ARTWORK/s
    # json_file = json.load(open('./static/assets/json/artpedia.json', 'rb'))
    # import_datas(json_file, Artwork)

    return render(request, "index.html", {'artwork': obj, 'ga_key': ga_key})


def gallery_view(request, century=None, page=None):
    artwork = Artwork.objects.all().order_by('year')
    centuries = set([int(work.century) for work in artwork])
    century = request.GET.get('century')
    if century:
        artwork = artwork.filter(century=century)
    p = Paginator(artwork, 40)
    page = request.GET.get('page')
    try:
        page_obj = p.page(page)
    except PageNotAnInteger:
        print("PageNotAnInteger")
        page_obj = p.page(1)
        page = 1
    except EmptyPage:
        print("EmptyPage")
        page_obj = p.page(p.num_pages)
        page = p.num_pages

    context = {
        'artwork': artwork,
        'page_obj': page_obj,
        'ga_key': ga_key,
        'centuries': sorted(centuries),
        'current_century': int(century) if century else "",
        'page_number': page
    }

    return render(request, "gallery.html", context)


class ArtworkDetails(View):
    art = "momentaneo"

    def get(self, request):
        obj = Question_Answer.objects.all()
        questions = []
        for element in obj:
            if element.title == self.art.title:
                questions.append(element)
        context = {'artwork': self.art, 'question': questions, 'chat_link': self.art.link + '/chat/', 'ga_key': ga_key}
        return render(request, "gallery-details.html", context)


class Artworkchat(View):
    art = "tmp"

    def post(self, request):
        context = {'artwork': self.art, 'ga_key': ga_key}
        return render(request, "artwork-chat.html", context)

    def get(self, request):
        context = {'artwork': self.art, 'ga_key': ga_key}
        return render(request, "artwork-chat.html", context)


@csrf_exempt
def handle_chat_question(request):
    print('in handle question')
    img_url = request.POST["img"]
    question = request.POST["question"]
    artwork = Artwork.objects.get(image=img_url)
    print('get image url')
    v_desc = artwork.visual_description
    c_desc = artwork.contextual_description
    title = artwork.title
    year = " this painting was depicted in " + str(artwork.year)
    text_info = c_desc + year + ' ' + v_desc
    img_feats = img_url
    print('setting data info')
    answer = AnswerGenerator().produce_answer(question, title, str(artwork.year), text_info, img_feats)

    return JsonResponse({'answer': answer})


def chat_view(request):
    return render(request, "chat.html")
