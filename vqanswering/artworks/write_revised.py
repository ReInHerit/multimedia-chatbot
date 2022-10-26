# from models import Question_Answer
# from models import Artwork

# qa = Question_Answer.objects.filter(revised="True")
# artwork = Artwork.objects.all
def write_revised(question, artworks):
    qa = question
    artwork = artworks
    j = 1
    w_dic = dict()
    for element in qa:
        for details in artwork:
            if element.title == details.title:
                art = details
        qa_dic = {'title': element.title, 'image_url': art.image, 'question': element.question,
                  'answer': element.answer, 'sentence_type': element.sentence_type}
        ext_dic = {j: qa_dic}
        w_dic.update(ext_dic)
        j = j + 1
    return w_dic
# with open("/home/frenk/vqanswering/artworks/revised_qa.json", 'w') as outfile:
# 	outfile.write("{}\n".format(json.dumps(w_dic)))
