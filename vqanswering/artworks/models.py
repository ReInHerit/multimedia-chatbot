from django.db import models

class Artwork(models.Model):
	title = models.CharField(max_length = 150)
	image = models.URLField()
	thumb_image = models.URLField()
	year = models.DecimalField(max_digits=4, decimal_places=0)
	visual_description = models.TextField()
	contextual_description = models.TextField()
	century = models.IntegerField()
	link = models.CharField(max_length = 200)



class Suggestion(models.Model):
	name = models.CharField(max_length = 200)
	email = models.EmailField()
	subject = models.CharField(max_length = 200)
	message = models.TextField()

class Question_Answer(models.Model):
	GENERATION_CHOICES = (
		("human generated", "human generated"),
		("auto generated", "auto generated")
		)
	TYPE_CHOICES = (
		("visual sentence", "visual sentence"),
		("contextual sentence", "contextual sentence")
		)
	MISTAKE_QUESTION_CHOICES = (
	("One character question", "One character question"),
	("Too long question", "Too long question"),
	("What is? as question or two words question", "What is? as question or two words question"),
	("Commission related wrong question", "Commission related wrong question"),
	("Who instead of Where or viceversa", "Who instead of Where or viceversa"),
	("What instead of Where or viceversa", "What instead of Where or viceversa"),
	("Was instead of were or viceversa", "Was inted of were or viceversa"),
	("Part of the sentence repeated", "Part of the sentence repeated"),
	("Indefinite article instead of definite article or viceversa", "Indefinite article instead of definite article or viceversa"),
	("No sense question", "No sense question"),
	("Correct", "Correct"),
	("Unrevised", "Unrevised")
	)
	MISTAKE_ANSWER_CHOICES = (
	("Pronoun as answer", "Pronoun as answer"),
	("The painting, the work or similiar as answer", "The painting, the work or similiar as answer"),
	("One character answer", "One character answer"),
	("Commission related wrong answer", "Commission related wrong answer"),
	("Was instead of were or viceversa", "Was inted of were or viceversa"),
	("Part of the sentence repeated", "Part of the sentence repeated"),
	("Indefinite article instead of definite article or viceversa", "Indefinite article instead of definite article or viceversa"),
	("First as answer", "First as answer"),
	("Now as answer", "Now as answer"),
	("No sense number as answer", "No sense number as answer"),
	("No sense answer", "No sense answer"),
	("Correct", "Correct"),
	("Unrevised", "Unrevised")
	)
	title = models.CharField(max_length = 300)
	question = models.TextField()
	answer = models.TextField()
	generation = models.CharField(max_length = 50, choices = GENERATION_CHOICES)
	sentence_type = models.CharField(max_length = 150, choices = TYPE_CHOICES, default= "contextual sentence")
	revised = models.BooleanField(default=False)
	to_show = models.BooleanField(default=True)
	dataset_version = models.CharField(max_length = 300, default="first version")
	question_error_type = models.CharField(max_length=500, default = "Unrevised", choices=MISTAKE_QUESTION_CHOICES)
	answer_error_type = models.CharField(max_length=500, default = "Unrevised", choices=MISTAKE_ANSWER_CHOICES)