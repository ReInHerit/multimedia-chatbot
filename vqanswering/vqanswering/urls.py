from django.contrib import admin
from django.urls import path
from artworks.views import home_view, gallery_view, handle_chat_question, Artworkchat,  admin_home, add_artworks_via_wikipedia, add_artworks_from_json
from artworks.models import Artwork

# app_name = 'myapp'
urlpatterns = [
    path('', home_view, {}, name='home_view'),
    path('admin/', admin.site.urls),
    path('gallery/', gallery_view, name='gallery_view'),
    path('handle_chat_question/', handle_chat_question, name='handle_chat'),
    path('admin/', admin_home, name='admin_home'),
    path('add-artworks-from-json/', add_artworks_from_json, name='add_artworks_from_json'),
    path('add-artworks-via-wikipedia/', add_artworks_via_wikipedia, name='add_artworks_via_wikipedia'),
]

obj = Artwork.objects.all()

for article in obj:
    link = 'gallery/' + article.link + '/'
    urlpatterns.append(path(link, Artworkchat.as_view(art=article)))
