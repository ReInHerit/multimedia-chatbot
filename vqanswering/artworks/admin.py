from django.contrib import admin
from django.utils.html import format_html
from .models import Artwork, Chat

# admin.py
from django.http import HttpResponseRedirect
from django.urls import reverse


class ArtworkAdmin(admin.ModelAdmin):
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

class ChatAdmin(admin.ModelAdmin):
    list_display = ('artwork', 'question', 'answer', 'question_language', 'resolved',)
    list_filter = ('resolved', 'question_language',)
    search_fields = ('question', 'answer',)

    actions = ['delete_selected_chats']

    # def download_database_dump(self, request, queryset):
    #     return HttpResponseRedirect(reverse('database_dump'))
    #
    # download_database_dump.short_description = 'Download database dump'
    #
    # def response_action(self, request, queryset):
    #     if "download_database_dump" in request.POST:
    #         return self.download_database_dump(request, queryset)
    #     return super().response_action(request, queryset)


admin.site.register(Chat, ChatAdmin)
admin.site.site_header = 'ReInHerit VIOLA Admin'
admin.site.register(Artwork, ArtworkAdmin)

