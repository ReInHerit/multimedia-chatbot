import os

from django.contrib import admin
from django.utils.html import format_html
from .models import Artwork, Chat
from django import forms
# admin.py
from django.http import HttpResponseRedirect
from django.urls import reverse

from utils.download_thumbs import create_thumb


class ArtworkAdminForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = '__all__'
        widgets = {
            'image': forms.TextInput(attrs={'readonly': 'readonly'}),
            'thumb_image': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class ArtworkAdmin(admin.ModelAdmin):
    form = ArtworkAdminForm
    list_display = ('title', 'year', 'century',)
    list_filter = ('century', 'year',)
    search_fields = ('title', 'year', 'century',)
    readonly_fields = ('link',)  # Make the 'link' field read-only in the admin page

    def save_model(self, request, obj, form, change):
        obj.link = obj.title.replace(' ', '_')
        if not obj.id:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

        if 'user_image' in form.changed_data:
            # If the user has uploaded a new image, then save the image and create the thumbnail
            # Save the image file to the server
            print('obj.user_image.path', obj.user_image.path)
            print('obj.user_image.name', obj.user_image.name)
            file_name = os.path.basename(obj.user_image.path)
            # Now that the image file is saved, you can create the thumbnail.
            thumb_path = create_thumb(obj.user_image.path, file_name)
            # Update the image and thumb_image fields
            obj.image = "/static/assets/img/full/" + file_name
            obj.thumb_image = "/static/assets/img/thumbs/" + file_name
            # Save the object again to save the changes to the image and thumb_image fields.
            obj.save()

class ChatAdmin(admin.ModelAdmin):
    list_display = ('artwork', 'question', 'answer', 'question_language', 'resolved',)
    list_filter = ('resolved', 'question_language',)
    search_fields = ('question', 'answer',)

    actions = ['delete_selected_chats']


admin.site.register(Chat, ChatAdmin)
admin.site.site_header = 'ReInHerit VIOLA Admin'
admin.site.register(Artwork, ArtworkAdmin)

