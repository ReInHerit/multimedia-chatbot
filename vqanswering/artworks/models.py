from django.db import models


class Artwork(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    image = models.URLField()
    thumb_image = models.URLField()
    year = models.DecimalField(max_digits=4, decimal_places=0)
    visual_description = models.TextField()
    contextual_description = models.TextField()
    century = models.IntegerField()
    link = models.CharField(max_length=200)
