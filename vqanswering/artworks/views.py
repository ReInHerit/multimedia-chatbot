from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import Artwork
from .models import Suggestion
from .models import Question_Answer
from .forms import QAForm
from django.views import View
import json
from random import randint
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .answer_generator import AnswerGenerator

answer_generator = AnswerGenerator()


def home_view(request):
	obj = Artwork.objects.all()
	context = {
		'artwork': obj
	}

	return render(request, "index.html", context)


def gallery_view(request):
	obj = Artwork.objects.all()
	context = {'artwork': obj}

	t = Artwork.objects.get(id=24625)
	t.contextual_description = [
		'Bridal Procession on the Hardanger (Norwegian: Brudeferd i Hardanger) is one of the best known Norwegian '
		'paintings.',
		'The 1848 painting was painted by the authors Hans Gude and Adolph Tidemand.',
		'Gude painted the landscapes and Tidemand the bridal party.',
		'The painting is 93 x 130 cm, and is in the National Gallery in Oslo.',
		'The painting is considered to be an excellent example of romantic nationalism in Norway.',
		'The scene, Gude later wrote, was not as viewed from a particular location, but was deliberately composed from '
		'his overall observations.',
		'The painting was first presented in a tableau vivant at the Christiania Theater in 1849.',
		'The soireé, in March 1849, included a theatrical group dressed in traditional costumes aboard a boat who '
		'performed a song by Andreas Munch with music by Halfdan Kjerulf, with the painting itself serving as scenery.']
	#  change field
	t.save()
	print(t.contextual_description)
	return render(request, "gallery.html", context)


def add_suggestion(request):
	name = request.POST["name"]
	email = request.POST["email"]
	subject = request.POST["subject"]
	message = request.POST["message"]

	suggestion = Suggestion(name=name, email=email, subject=subject, message=message)
	suggestion.save()
	return redirect("/home/#contact")


class ArtworkDetails(View):
	art = "momentaneo"

	def get(self, request):
		obj = Question_Answer.objects.all()
		questions = []
		for element in obj:
			if element.title == self.art.title:
				questions.append(element)
		
		context = {'artwork': self.art, 'question': questions, 'chat_link': self.art.link + '/chat/'}
		return render(request, "gallery-details.html", context)


class Artworkchat(View):
	art = "tmp"

	def post(self, request):
		#  print(request['question'])
		context = {'artwork': self.art}
		return render(request, "artwork-chat.html", context)

	def get(self, request):
		context = {'artwork': self.art}
		return render(request, "artwork-chat.html", context)


def qa_revision(request):
	qa = Question_Answer.objects.all()
	count = qa.count()
	i = randint(0, count-1)
	while qa[i].revised is True or qa[i].to_show is False:
		i = randint(0, count-1)
	artwork = Artwork.objects.get(title=qa[i].title)
	context = {'artwork': artwork, 'q': qa[i]}
	return render(request, "random_revision.html", context)


def add_questionanswer(request):
	title = request.POST["title"]
	question = request.POST["question"]
	answer = request.POST["answer"]
	sentence_type = request.POST["sent_type"]

	new_qa = Question_Answer(title=title, question=question, answer=answer, generation="human generated")
	new_qa.save()
	link = str(title)
	new_link = link.replace(" ", "-")
	link = '/home/' + new_link + "/" + "#questionanswer"

	return redirect(link)


def post_edit(request, pk):
	qa = get_object_or_404(Question_Answer, pk=pk)
	if request.method == "POST":
		form = QAForm(request.POST, instance=qa)
		if form.is_valid():
			qa = form.save(commit=False)
			qa.question = request.POST["question"]
			qa.answer = request.POST["answer"]
			qa.generation = "human generated"
			qa.save()
			link = str(qa.title)
			newlink = link.replace(" ", "-")
			link = '/home/' + newlink + "/" + "#questionanswer"
			return redirect(link)
	else:
		form = QAForm(instance=qa)
	return render(request, 'qa_edit.html', {'form': form})


def qa_delete(request, pk):
	qa = get_object_or_404(Question_Answer, pk=pk)
	qa.delete()
	link = str(qa.title)
	newlink = link.replace(" ", "-")
	link = '/home/' + newlink + "/" + "#questionanswer"
	return redirect(link)


def revided(request, pk):
	qa = get_object_or_404(Question_Answer, pk=pk)
	qa.revised = True
	qa.answer_error_type = "Correct"
	qa.question_error_type = "Correct"
	qa.save()
	return redirect('/home/random_revision')


def qa_delete_rand(request, pk):
	qa = get_object_or_404(Question_Answer, pk=pk)
	qa.to_show = False
	qa.question_error_type = "No sense question"
	qa.answer_error_type = "No sense answer"
	qa.save()
	link = '/home/random_revision'
	return redirect(link)

def revision_edit(request, pk):
	qa = get_object_or_404(Question_Answer, pk=pk)
	if request.method == "POST":
		form = QAForm(request.POST, instance=qa)
		if form.is_valid():
			qa = form.save(commit=False)
			qa.question = request.POST["question"]
			qa.answer = request.POST["answer"]
			qa.generation = "human generated"
			qa.revised = True
			qa.answer_error_type = request.POST["answer_error_type"]
			qa.question_error_type = request.POST["question_error_type"]			
			qa.save()
			link = str(qa.title)
			newlink = link.replace(" ", "-")
			link = '/home/random_revision'
			return redirect(link)
	else:
		form = QAForm(instance = qa)
	return render(request, 'revision-edit.html', {'form':form})

def revision_result(request):
	obj = Question_Answer.objects
	context = {

		"question_revised": obj.filter(revised=True).count()+ obj.filter(to_show=False).count(),
		"question_correct":obj.filter(revised=True).count(),

		"primaQ": 2+obj.filter(question_error_type="One character question").count(),
		"secondaQ": 145+obj.filter(question_error_type="Too long question").count(),
		"terzaQ": 80+obj.filter(question_error_type="What is? as question or two words question").count(),
		"quartaQ": 6+obj.filter(question_error_type="Commission related wrong question").count(),
		"quintaQ": 2+obj.filter(question_error_type="Who instead of Where or viceversa").count(),
		"sestaQ": 4+obj.filter(question_error_type="What instead of Where or viceversa").count(),
		"settimaQ": 1+obj.filter(question_error_type="Was instead of were or viceversa").count(),
		"ottavaQ": 16+obj.filter(question_error_type="Part of the sentence repeated").count(),
		"nonaQ": 2+obj.filter(question_error_type="Indefinite article instead of definite article or viceversa").count(),
		"decimaQ": 448+obj.filter(question_error_type="No sense question").count(),
		"CorrectQ": 1000+obj.filter(question_error_type="Correct").count(),
		"UnrevisedQ": obj.filter(question_error_type="Unrevised").count(),

		"primaA":138+obj.filter(answer_error_type="Pronoun as answer").count(),
		"secondaA":68+obj.filter(answer_error_type="The painting, the work or similiar as answer").count(),
		"terzaA":2+obj.filter(answer_error_type="One character answer").count(),
		"quartaA":6+obj.filter(answer_error_type="Commission related wrong answer").count(),
		"quintaA":1+obj.filter(answer_error_type="Was instead of were or viceversa").count(),
		"sestaA":16+obj.filter(answer_error_type="Part of the sentence repeated").count(),
		"settimaA":2+obj.filter(answer_error_type="Indefinite article instead of definite article or viceversa").count(),
		"ottavaA":9+obj.filter(answer_error_type="First as answer").count(),
		"nonaA":6+obj.filter(answer_error_type="Now as answer").count(),
		"decimaA":28+obj.filter(answer_error_type="No sense number as answer").count(),
		"undicesimaA":448+obj.filter(answer_error_type="No sense answer").count(),
		"CorrectA":1000+obj.filter(answer_error_type="Correct").count(),
		"UnrevisedA":obj.filter(answer_error_type="Unrevised").count()
	}
	return render(request, "revision-result.html", context)

@csrf_exempt
def handle_chat_question(request):
	img_url = request.POST["img"]
	question = request.POST["question"]
	artwork = Artwork.objects.get(image= img_url)
	v_desc = artwork.visual_description
	c_desc = artwork.contextual_description
	year = "this painting was depicted in " + str(artwork.year)
	text_info = c_desc + year + v_desc
	#img_feats = answer_generator.get_image_features(img_url)
	img_feats = img_url
	print(img_feats)
	answer = answer_generator.produceAnswer(question, text_info, img_feats)
	return JsonResponse({'answer':answer})#render(request, "chat.html")#{'answer': answer}

def chat_view(request):
	return  render(request, "chat.html")