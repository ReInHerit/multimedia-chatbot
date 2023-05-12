from django.contrib import admin
from .models import Artwork


class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'century',)
    list_filter = ('century', 'year',)
    search_fields = ('title', 'year', 'century',)

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Artwork, ArtworkAdmin)
