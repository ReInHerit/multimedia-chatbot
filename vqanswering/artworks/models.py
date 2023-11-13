from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .signals import delete_artwork_images


class Artwork(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    year = models.CharField(max_length=7, default="Unknown")
    century = models.CharField(max_length=7, default="Unknown")
    time_period = models.CharField(max_length=200, null=True, blank=True, default="Unknown")
    image = models.CharField(max_length=200)
    thumb_image = models.CharField(max_length=200)
    subject = models.CharField(max_length=200, default="Unknown")
    type_of_object = models.CharField(max_length=200, default="Unknown")
    measurement = models.CharField(max_length=200, default="Unknown")
    maker = models.CharField(max_length=200, default="Unknown")
    materials_and_techniques = models.CharField(max_length=200, default="Unknown")
    location = models.CharField(max_length=200, default="Unknown")
    description = models.TextField()
    web_link = models.CharField(max_length=250, default="-", blank=True)
    link = models.CharField(max_length=200, default="-")


# Connect the signal receiver to the pre_delete signal of Artwork
pre_delete.connect(delete_artwork_images, sender=Artwork)
