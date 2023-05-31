import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver

here = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(here)
@receiver(pre_delete, sender='artworks.Artwork')
def delete_artwork_images(sender, instance, **kwargs):
    thumb_path = project_root + instance.thumb_image
    full_path = project_root + instance.image

    if os.path.exists(thumb_path):
        os.remove(thumb_path)

    if os.path.exists(full_path):
        os.remove(full_path)
