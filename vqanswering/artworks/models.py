from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .signals import delete_artwork_images


class Artwork(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    thumb_image = models.CharField(max_length=200)
    year = models.DecimalField(max_digits=4, decimal_places=0)
    description = models.TextField()
    century = models.IntegerField()
    link = models.CharField(max_length=200)
    wiki_url = models.URLField(default='', blank=True)


# Connect the signal receiver to the pre_delete signal of Artwork
pre_delete.connect(delete_artwork_images, sender=Artwork)
