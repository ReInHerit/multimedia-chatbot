from bert import get_pretrained_bert

question = 'how many people are in the image?'
question_classifier = get_pretrained_bert()
predictions, raw_outputs = question_classifier.predict([question])
print(predictions)
