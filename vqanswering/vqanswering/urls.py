from django.contrib import admin
from django.urls import path, include
from artworks.views import home_view, gallery_view, handle_chat_question, Artworkchat, database_dump, admin_home, add_artworks_via_folder

urlpatterns = [
    path('', home_view, {}, name='home_view'),
    path('admin/database_dump/', database_dump, name='database_dump'),
    path('admin/', admin.site.urls),
    path('gallery/', gallery_view, name='gallery_view'),
    path('handle_chat_question/', handle_chat_question, name='handle_chat'),
    path('admin/', admin_home, name='admin_home'),
    path('add-artworks-via-folder/', add_artworks_via_folder, name='add_artworks_via_folder'),
    path('', include('artworks.urls')),
]


