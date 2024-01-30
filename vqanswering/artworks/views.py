import os
import math

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Artwork
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .answer_generator import AnswerGenerator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
import re
import requests
from utils.download_thumbs import create_thumb

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
    url = request.POST.get("url")
    question = request.POST.get("question")

    if not url or not question:
        return JsonResponse({'answer': 'Invalid request'})

    address_title = url.rsplit('gallery/')[1][:-1]
    title = address_title.replace('_', ' ')

    artwork = Artwork.objects.filter(title__iexact=title).first()

    if artwork is None:
        return JsonResponse({'answer': 'Artwork not found'})

    context = artwork.description
    answer = AnswerGenerator().produce_answer(question, title, context)

    return JsonResponse({'answer': answer})


@login_required
@staff_member_required
def admin_home(request):
    return render(request, 'admin_home.html')


@csrf_exempt
def add_artworks_via_folder(request):
    if request.method == 'POST':
        admin_files_directory = 'static/assets/img/add_new_files/'

        # List files in the directory
        file_list = os.listdir(admin_files_directory)
        print("file_list", file_list)
        # Process the files as needed
        text_files = []
        image_files = []
        for file in file_list:
            if file.endswith(".txt"):
                text_files.append(file)
            elif file.endswith(".jpg") or file.endswith(".png"):
                image_files.append(file)

        for file in image_files:
            file_path = os.path.join(admin_files_directory, file)
            create_thumb(file_path, file)

            masterpiece = file.split('.')[0]
            title = masterpiece.replace('_', ' ')
            txt_file_path = os.path.join(admin_files_directory, masterpiece + ".txt")
            with open(txt_file_path, "r", encoding='utf-8') as txt_file:
                description = txt_file.read()

            regex_patterns = {
                'Time Period': r"Date: (.+)",
                'Measurement': r"Measurement: (.+)",
                'Maker': r"Maker: (.+)",
                'Materials and Techniques': r"Materials and techniques: (.+)",
                'Location': r"Location: (.+)",
                'Subject': r"Subject: (.+)",
                'Type of Object': r"Type of object: (.+)",
                'Link': r"Link: (.+)",
            }

            extracted_data = {}
            for key, pattern in regex_patterns.items():
                match = re.search(pattern, description)
                if match:
                    extracted_data[key] = match.group(1)
                else:
                    extracted_data[key] = "Unknown"
            time_period, year, century = find_year_century_from_period(extracted_data['Time Period'])

            artwork = Artwork(
                title=title,
                image="/static/assets/img/full/" + file,
                thumb_image="/static/assets/img/thumbs/" + file,
                year=year,
                description=description,
                time_period=time_period,
                measurement=extracted_data['Measurement'],
                maker=extracted_data['Maker'],
                materials_and_techniques=extracted_data['Materials and Techniques'],
                location=extracted_data['Location'],
                subject=extracted_data['Subject'],
                type_of_object=extracted_data['Type of Object'],
                century=century,
                web_link=extracted_data['Link'],
                link=masterpiece,
            )
            artwork.save()

        return JsonResponse({'success': True})


def find_year_century_from_period(time_period):
    year = "Unknown"
    century = "Unknown"
    print("time_period", time_period)
    new_time_period = time_period
    if time_period:
        time_period = time_period.strip().lower()
        year_matches = re.findall(r'\d{1,4}', time_period)
        parts = time_period.split()
        if len(year_matches) == 1:
            # Check if the input represents a century
            if len(parts) == 2 and parts[1] == 'century':
                century = int(year_matches[0])
                new_time_period = year_matches[0] + "th century"
            elif 'today' in time_period:
                # If 'today' is present, assume CE and calculate the century based on the start year
                start_year = int(year_matches[0])
                century = math.ceil(start_year / 100)
                new_time_period = f"{start_year} CE – today"
            else:
                year = year_matches[0]
                # Check the last part of the input to determine BCE or CE
                if parts[-1] in ("bc", "bce"):
                    year = "-" + year
                    century = math.ceil(int(year) / 100) - 1
                    new_time_period = year_matches[0] + " BCE"
                elif parts[-1] in ("ad", "ce"):
                    century = math.ceil(int(year) / 100)
                    new_time_period = year_matches[0] + " CE"
                else:
                    century = math.ceil(int(year) / 100)
                    new_time_period = year_matches[0] + " CE"
        elif len(year_matches) == 2:
            start_year, end_year = map(int, year_matches)

            if abs(end_year - start_year) <= 100:
                century = math.ceil(start_year / 100)
                new_time_period = f"{start_year} - {end_year} CE"
                if parts[-1] in ("bc", "bce"):
                    century = math.ceil(int(end_year) / 100)
                    century = f"-{century}"
                    new_time_period = f"{start_year} - {end_year} BCE"
                elif parts[-1] in ("ad", "ce"):
                    century = math.ceil(start_year / 100)
                    new_time_period = f"{start_year} - {end_year} CE"
    print("new_time_period", new_time_period, year, century)
    return new_time_period, year, century
def check_url(url):
    try:
        response = requests.head(url)
        return response.status_code == requests.codes.ok
    except requests.exceptions.RequestException:
        return False