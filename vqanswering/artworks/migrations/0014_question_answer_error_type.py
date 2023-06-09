# Generated by Django 3.1 on 2020-09-26 14:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('artworks', '0013_question_answer_dataset_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='question_answer',
            name='error_type',
            field=models.CharField(choices=[('Pronoun as answer', 'Pronoun as answer'),
                                            ('The painting, the work or similiar as answer',
                                             'The painting, the work or similiar as answer'),
                                            ('One character question', 'One character question'),
                                            ('One character answer', 'One character answer'),
                                            ('Too long question', 'Too long question'),
                                            ('Used wrongly subject instead of object or viceversa',
                                            'Used wrongly subject instead of object or viceversa'),
                                            ('Commission related wrong question', 'Commission related wrong question'),
                                            ('Who instead of Where or viceversa', 'Who instead of Where or viceversa'),
                                            ('What instead of Where or viceversa',
                                             'What instead of Where or viceversa'),
                                            ('Was inted of were or viceversa', 'Was inted of were or viceversa'),
                                            ('Part of the sentence repeated', 'Part of the sentence repeated'),
                                            ('Indefinite article instead of definite article or viceversa',
                                            'Indefinite article instead of definite article or viceversa'),
                                            ('First as answer', 'First as answer'), ('Now as answer', 'Now as answer'),
                                            ('No sense number as answer', 'No sense number as answer'),
                                            ('No sense answer', 'No sense answer'), ('Correct', 'Correct'),
                                            ('Unrevised', 'Unrevised')], default='Unrevised', max_length=500),
        ),
    ]
