import io
import math
import urllib.parse
import io
import json
import math
import urllib.parse

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from .forms import ImportArtworksForm
from .models import Artwork
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .answer_generator import AnswerGenerator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse, reverse_lazy
from django.conf import settings

ga_key = settings.GA_MEASUREMENT_ID


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


@csrf_exempt
def add_artworks_from_json(request):
    if request.method == 'POST':
        json_file = request.FILES['json_file']
        print("json_path", json_file)
        try:
            json_data = json.load(io.TextIOWrapper(json_file))
            for article_id in json_data:
                file_name = urllib.parse.quote(json_data[article_id]['img_url'].split("/")[-1], safe="")
                century = (json_data[article_id]['year'] // 10 ** (int(math.log(json_data[article_id]['year'], 10)) - 1)) * 100
                link = str(json_data[article_id]['title']).replace(" ", "-")
                artwork = Artwork(
                    title=json_data[article_id]['title'],
                    image="/static/assets/img/full/" + file_name,
                    thumb_image="/static/assets/img/thumbs/" + file_name,
                    year=json_data[article_id]['year'],
                    visual_description=json_data[article_id]['visual_sentences'],
                    contextual_description=json_data[article_id]['contextual_sentences'],
                    century=century,
                    link=link,
                )
                artwork.save()

            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON file'})
    else:
        return JsonResponse({'success': False, 'message': 'No file uploaded'})


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
    # eliminate gostname and keep from /static/...
    img_url = '/static' + img_url.split('static')[1]
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


@login_required
@staff_member_required
def admin_home(request):
    return render(request, 'admin_home.html')


# class ArtworkImport(FormView):
#     form_class = ImportArtworksForm
#     # template_name = 'import_artworks.html'
#     success_url = reverse_lazy('admin:artwork_artwork_changelist')
#
#     def form_valid(self, form):
#         file = form.cleaned_data['file']
#         artworks = form.process_data(file)
#
#         if artworks:
#             for artwork in artworks:
#                 Artwork.objects.create(
#                     title=artwork['title'],
#                     image=artwork['image'],
#                     thumb_image=artwork['thumb_image'],
#                     year=artwork['year'],
#                     visual_description=artwork['visual_description'],
#                     contextual_description=artwork['contextual_description'],
#                     century=artwork['century'],
#                     link=artwork['link'],
#                 )
#             messages.success(self.request, f'Successfully imported {len(artworks)} artworks.')
#         else:
#             messages.warning(self.request, 'No artworks were imported.')
#
#         return super().form_valid(form)