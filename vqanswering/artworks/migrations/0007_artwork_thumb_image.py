# Generated by Django 3.1 on 2020-09-02 10:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('artworks', '0006_artwork_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='thumb_image',
            field=models.URLField(default='www.google.com'),
            preserve_default=False,
        ),
    ]
