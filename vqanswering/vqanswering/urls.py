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
from artworks.views import home_view, add_suggestion, gallery_view, add_questionanswer, post_edit
from artworks.models import Artwork
from artworks.views import ArtworkDetails, qa_delete, qa_revision, revision_edit, qa_delete_rand, revided, \
    revision_result, handle_chat_question
from artworks.views import chat_view, Artworkchat

urlpatterns = [
    path('home/', home_view, {}),
    path('admin/', admin.site.urls),
    path('add_suggestion/', add_suggestion, name='add_suggestion'),
    path('home/gallery', gallery_view),
    path('add_questionanswer/', add_questionanswer),
    path('home/<int:pk>/edit/', post_edit, name='post_edit'),
    path('home/<int:pk>/remove/', qa_delete, name='qa_delete'),
    path('home/random_revision/', qa_revision),
    path('home/<int:pk>/revision_edit', revision_edit, name="revision_edit"),
    path('home/<int:pk>/remove_rand/', qa_delete_rand, name='qa_delete_rand'),
    path('home/<int:pk>/random_revision', revided, name="revided"),
    path('home/revision_result', revision_result),
    path('home/chat', chat_view),
    path('handle_chat_question/', handle_chat_question, name='handle_chat')
]

obj = Artwork.objects.all()
for article in obj:
    link = 'home/' + article.link + '/'
    link_chat = link + 'chat/'
    urlpatterns.append(path(link, ArtworkDetails.as_view(art=article)))
    urlpatterns.append(path(link_chat, Artworkchat.as_view(art=article)))
