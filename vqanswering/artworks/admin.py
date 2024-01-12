from django.contrib import admin
from django.utils.html import format_html
from .models import Artwork


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

admin.site.site_header = 'ReInHerit VIOLA Admin'
admin.site.register(Artwork, ArtworkAdmin)

