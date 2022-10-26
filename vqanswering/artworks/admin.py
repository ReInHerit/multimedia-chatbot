from django.contrib import admin

from .models import Artwork, Suggestion, Question_Answer

admin.site.register(Artwork)
admin.site.register(Suggestion)
admin.site.register(Question_Answer)

# Register your models here.
