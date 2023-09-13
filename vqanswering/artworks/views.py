import os
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


def gallery_view(request, page=None):
    artwork = Artwork.objects.all().order_by('title')

    # Create a list of unique letters in artwork titles
    title_starting_letters = set([work.title[0].upper() for work in artwork if work.title])

    # Get the starting letter from the query parameter 'letter'
    letter = request.GET.get('letter', None)
    if letter:
        artwork = artwork.filter(title__istartswith=letter)

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
        'starting_letters': sorted(title_starting_letters),
        'current_letter': letter.upper() if letter else "",
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

# @csrf_exempt
# def add_artworks_from_json(request):
#     if request.method == 'POST':
#         json_file = request.FILES['json_file']
#         print("json_path", json_file)
#         try:
#             json_data = json.load(io.TextIOWrapper(json_file))
#             for article_id in json_data:
#                 wiki_title = json_data[article_id]['wiki_title']
#                 file_name = sanitize_file_name(wiki_title)
#                 file_name = file_name + '.jpg'
#
#                 create_thumb(json_data[article_id]['image_url'], file_name)
#
#                 century = (int(json_data[article_id]['year']) // 10 **
#                            (int(math.log(int(json_data[article_id]['year']), 10)) - 1)) * 100
#
#                 artwork = Artwork(
#                     title=json_data[article_id]['title'],
#                     image="/static/assets/img/full/" + file_name,
#                     thumb_image="/static/assets/img/thumbs/" + file_name,
#                     year=json_data[article_id]['year'],
#                     description=json_data[article_id]['context'],
#                     century=century,
#                     link=wiki_title,
#                     wiki_url=json_data[article_id]['wiki_url'],
#                 )
#                 artwork.save()
#
#             return JsonResponse({'success': True})
#         except json.JSONDecodeError:
#             return JsonResponse({'success': False, 'message': 'Invalid JSON file'})
#     else:
#         return JsonResponse({'success': False, 'message': 'No file uploaded'})
#
# @csrf_exempt
# def add_artworks_via_wikipedia(request):
#     if request.method == 'POST':
#         wikipedia.set_lang("en")
#         wiki_url = request.POST.get('url')
#         print("url", wiki_url)
#         wiki_title = wiki_url.rsplit('wiki/')[1]
#         title = wiki_title.replace('_', ' ')
#
#         main_image_source = get_image_url(title, wiki_url)
#         file_name = sanitize_file_name(wiki_title) + '.jpg'
#         create_thumb(main_image_source, file_name)
#         print('wiki_title', wiki_title)
#         wiki_page = wikipedia.WikipediaPage(wiki_title)
#         year = get_year(wiki_title)
#         context = get_context(wiki_page)
#         if year:
#             century = (int(year) // 10 ** (int(math.log(int(year), 10)) - 1)) * 100
#         else:
#             century = int(3000)
#         artwork = Artwork(
#             title=title,
#             wiki_url=wiki_url,
#             year=year,
#             image="/static/assets/img/full/" + file_name,
#             thumb_image="/static/assets/img/thumbs/" + file_name,
#             description=context,
#             century=century,
#             link=wiki_title,
#         )
#         artwork.save()
#         return JsonResponse({'success': True})

@csrf_exempt
def add_artworks_via_folder(request):
    if request.method == 'POST':
        admin_files_directory = 'static/assets/img/add_new_files/'

        # List files in the directory
        file_list = os.listdir(admin_files_directory)
        print("file_list", file_list)
        # Process the files as needed
        # processed_files = []
        # masterpieces = {}
        text_files = []
        image_files = []
        for file in file_list:
            # name_without_extension = file.split('.')[0]

            if file.endswith(".txt"):
                text_files.append(file)
            elif file.endswith(".jpg") or file.endswith(".png"):
                image_files.append(file)

        for file in image_files:
            file_path = os.path.join(admin_files_directory, file)
            create_thumb(file_path, file)

            masterpiece = file.split('.')[0]
            title = masterpiece.replace('_', ' ')
            with open(os.path.join(admin_files_directory, masterpiece + ".txt"), "r", encoding='utf-8') as txt_file:
                description = txt_file.read()
            # Define regular expressions to match each piece of information
            time_period_pattern = r"Date: (.+)"
            size_pattern = r"Measurement: (.+)"
            artist_pattern = r"Maker: (.+)"
            material_pattern = r"Materials and techniques: (.+)"
            institution_pattern = r"Location: (.+)"
            subject_pattern = r"Subject: (.+)"
            typeof_pattern = r"Type of object: (.+)"
            link_pattern = r"Link: (.+)"
            # Use regular expressions to extract data
            time_period_match = re.search(time_period_pattern, description)
            size_match = re.search(size_pattern, description)
            artist_match = re.search(artist_pattern, description)
            material_match = re.search(material_pattern, description)
            institution_match = re.search(institution_pattern, description)
            subject_match = re.search(subject_pattern, description)
            typeof_match = re.search(typeof_pattern, description)
            link_match = re.search(link_pattern, description)

            time_period = "Unknown"
            year = "Unknown"
            century = "Unknown"
            size = "Unknown"
            artist = "Unknown"
            material = "Unknown"
            institution = "Unknown"
            subject = "Unknown"
            typeof = "Unknown"
            link = "-"

            # Check if matches were found and extract the data
            if time_period_match:
                time_period = time_period_match.group(1)
                year, century = find_year_century_from_period(time_period)

            if size_match:
                size = size_match.group(1)

            if artist_match:
                artist = artist_match.group(1)

            if material_match:
                material = material_match.group(1)

            if institution_match:
                institution = institution_match.group(1)

            if subject_match:
                subject = subject_match.group(1)

            if typeof_match:
                typeof = typeof_match.group(1)

            if link_match:
                link = link_match.group(1)

            # Print the extracted data
            print("Time Period:", time_period)
            print("Year:", year)
            print("Century:", century)
            print("Measure:", size)
            print("Maker:", artist)
            print("Materials and techniques:", material)
            print("Location:", institution)
            print("Subject:", subject)
            print("Type of object:", typeof)
            print("Link:", link)

            artwork = Artwork(
                title=masterpiece.replace('_', ' '),
                image="/static/assets/img/full/" + file,
                thumb_image="/static/assets/img/thumbs/" + file,
                year=year,
                description=description,
                time_period=time_period,
                measurement=size,
                maker=artist,
                materials_and_techniques=material,
                location=institution,
                subject=subject,
                type_of_object=typeof,
                century=century,
                web_link=link,
                link=masterpiece,
            )
            artwork.save()

        return JsonResponse({'success': True})


def find_year_century_from_period(time_period):
    # Initialize year and century
    year = ""
    century = ""

    if time_period is None:
        # Case: time_period is None
        year = "Unknown"
        century = "Unknown"
    else:
        # Remove any extra spaces and convert to lowercase
        time_period = time_period.strip().lower()
        # Count the occurrences of \d{1,4} in time_period
        year_matches = re.findall(r'\d{1,4}', time_period)
        print("year_matches", year_matches, 'time_period', time_period)
        year_count = len(year_matches)
        if year_count == 2:
            # Case 1: Multiple years with BCE/CE
            year = "Unknown"
            century = "Unknown"
        elif year_count == 1:
            # Split time_period by spaces
            parts = time_period.split()
            print("parts", parts)
            if len(parts) == 1:
                # Case 2: Only a year is provided
                if len(parts[0]) == len(year_matches[0]):
                    year = year_matches[0]
                    century = math.ceil(int(year) / 100)
                else:
                    if parts[0].startswith("-") or parts[0].endswith("bc") or parts[0].endswith("bce"):
                        year = "-" + year_matches[0]
                        century = math.ceil(int(year) / 100) - 1
                    elif time_period.endswith("ad") or time_period.endswith("ce"):
                        year = year_matches[0]
                        century = math.ceil(int(year) / 100) + 1
                    else:
                        year = "Unknown"
                        century = "Unknown"
            elif len(parts) == 2:
                year = year_matches[0]
                if parts[0] == "-" or parts[1] == "bc" or parts[1] == "bce":
                    year = "-" + year
                    century = math.ceil(int(year) / 100) - 1
                elif parts[1] == "ad" or parts[1] == "ce":
                    century = math.ceil(int(year) / 100) + 1
                else:
                    year = "Unknown"
                    century = "Unknown"
            else:
                year = "Unknown"
                century = "Unknown"

    return year, century


def check_url(url):
    try:
        response = requests.head(url)
        return response.status_code == requests.codes.ok
    except requests.exceptions.RequestException:
        return False