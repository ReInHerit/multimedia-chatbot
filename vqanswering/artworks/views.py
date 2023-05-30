import urllib.parse
import io
import json
import math

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Artwork
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .answer_generator import AnswerGenerator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse, reverse_lazy
from django.conf import settings
import re
import requests
import wikipedia
from bs4 import BeautifulSoup
#import create_thumbs from static/assets/py/download_thumbs

from utils.download_thumbs import create_thumb
from utils.get_wiki_utilities import get_wikipage_from_title, get_context, get_image_url, get_year
ga_key = settings.GA_MEASUREMENT_ID
not_allowed_chars = r'[<>:"/\\|?*]'


def sanitize_file_name(title):
    # Remove special characters except for dot (.)
    title = re.sub(r'[^\w\s.-]', '', title)

    # Replace spaces and separators with underscores
    title = re.sub(r'\s+', '_', title)

    # Remove consecutive dots
    title = re.sub(r'\.+(?=\.)', '', title)

    # Truncate or abbreviate long titles
    max_length = 255  # Adjust as per your file system's limitations
    if len(title) > max_length:
        title = title[:max_length]

    # Normalize the file name
    title = title.lower()

    return title


def home_view(request):
    obj = Artwork.objects.all()

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
    url = request.POST["url"]
    question = request.POST["question"]
    wiki_title = url.rsplit('gallery/')[1][:-1]
    title = wiki_title.replace('_', ' ')
    wiki_url = 'https://en.wikipedia.org/wiki/' + wiki_title
    # Case-insensitive lookup using Q objects
    artwork = Artwork.objects.filter(Q(wiki_url__iexact=wiki_url) | Q(title__iexact=title)).first()
    if artwork is None:
        print('artwork is None')
        pass

    context = artwork.description
    answer = AnswerGenerator().produce_answer(question, title, context)

    return JsonResponse({'answer': answer})


@login_required
@staff_member_required
def admin_home(request):
    return render(request, 'admin_home.html')

@csrf_exempt
def add_artworks_from_json(request):
    if request.method == 'POST':
        json_file = request.FILES['json_file']
        print("json_path", json_file)
        try:
            json_data = json.load(io.TextIOWrapper(json_file))
            for article_id in json_data:
                wiki_title = json_data[article_id]['wiki_title']
                file_name= sanitize_file_name(wiki_title)
                file_name = file_name + '.jpg'

                create_thumb(json_data[article_id]['image_url'], file_name)

                century = (int(json_data[article_id]['year']) // 10 **
                           (int(math.log(int(json_data[article_id]['year']), 10)) - 1)) * 100

                artwork = Artwork(
                    title=json_data[article_id]['title'],
                    image="/static/assets/img/full/" + file_name,
                    thumb_image="/static/assets/img/thumbs/" + file_name,
                    year=json_data[article_id]['year'],
                    description=json_data[article_id]['context'],
                    century=century,
                    link=wiki_title,
                    wiki_url=json_data[article_id]['wiki_url'],
                )
                artwork.save()

            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON file'})
    else:
        return JsonResponse({'success': False, 'message': 'No file uploaded'})

@csrf_exempt
def add_artworks_via_wikipedia(request):
    excluded_titles = ["Notes", "References", "External links", "Further reading", "See also", "Sources", "Bibliography"]
    if request.method == 'POST':
        wikipedia.set_lang("en")
        wikipedia.BeautifulSoup(features="lxml")
        wiki_url = request.POST.get('url')
        print("url", wiki_url)
        wiki_title = wiki_url.rsplit('wiki/')[1]
        title = wiki_title.replace('_', ' ')

        main_image_source = get_image_url(title, wiki_url)
        file_name = sanitize_file_name(wiki_title) + '.jpg'
        create_thumb(main_image_source, file_name)
        print('wiki_title', wiki_title)
        wiki_page = wikipedia.WikipediaPage(wiki_title)
        year = get_year(wiki_title)
        context = get_context(wiki_page)
        if year:
            century = (int(year) // 10 ** (int(math.log(int(year), 10)) - 1)) * 100
        else:
            century = int(3000)
        artwork = Artwork(
            title=title,
            wiki_url=wiki_url,
            year=year,
            image="/static/assets/img/full/" + file_name,
            thumb_image="/static/assets/img/thumbs/" + file_name,
            description=context,
            century=century,
            link=wiki_title,
        )
        artwork.save()
        return JsonResponse({'success': True})

def check_url(url):
    try:
        response = requests.head(url)
        return response.status_code == requests.codes.ok
    except requests.exceptions.RequestException:
        return False