"""vqanswering URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from artworks.views import home_view, gallery_view, ArtworkDetails, handle_chat_question, chat_view, \
    Artworkchat
from artworks.models import Artwork

urlpatterns = [
    path('', home_view, {}, name='home_view'),
    path('admin/', admin.site.urls),
    path('gallery/', gallery_view, name='gallery_view'),
    path('chat/', chat_view),
    path('handle_chat_question/', handle_chat_question, name='handle_chat')
]

obj = Artwork.objects.all()

for article in obj:
    link = 'gallery/' + article.link + '/'
    link_chat = link + 'chat/'
    urlpatterns.append(path(link, ArtworkDetails.as_view(art=article)))
    urlpatterns.append(path(link_chat, Artworkchat.as_view(art=article)))
