from question_classifier.bert import get_pretrained_bert
import os
from PIL import Image
import requests
from transformers import DistilBertForQuestionAnswering, DistilBertTokenizer, ViltProcessor, ViltForQuestionAnswering
import torch
from google_trans_new import google_translator
from .git_vqa import generate_answers
import openai
import json
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
device = torch.device('cpu')
json_file = open('./static/assets/api-k.json')
key_data = json.load(json_file)
openai.api_key = key_data['openAI_key']
# models = openai.Model.list()
# print(models)
# Set up the model and prompt
model_engine = "text-davinci-003"
# model_engine = "text-curie-001"
def download_image(image_url):
    url = image_url
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/92.0.4515.159 Safari/537.36'}
    r = requests.get(url, headers=headers, stream=True)
    # Check if the image was retrieved successfully
    print(r.status_code)
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        img = Image.open(r.raw)
        return img
    else:
        return 0


class AnswerGenerator():
    def __init__(self):
        super(AnswerGenerator, self).__init__()

        self.question_classifier = get_pretrained_bert(use_cuda=False)
        self.translator = google_translator()  # Translator()
        device = torch.device('cpu')

        modelname = 'distilbert-base-uncased'

        self.vqamodel = DistilBertForQuestionAnswering.from_pretrained(
            'distilbert-base-uncased-distilled-squad')
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased',
                                                             return_token_type_ids=True)
        self.vqamodel.eval()
        self.vilt = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        self.vilt_processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        self.vilt.eval()

    def produceAnswer(self, question, artwork_title, year, context, vfeats):
        print(question)
        # prompt contextual
        # prompt = "Consider the painting " + artwork_title + " depicted in " + year + ". " + question + \
        #          " Respond with up to 30 words and consider first the following " \
        #          "information to respond: " + context + "if the answer is not in there, give me your."
        # prompt video
        prompt = "Consider the painting " + artwork_title + " depicted in " + year + ". " + question + \
                 "Respond with up to 30 words"
        # Generate a response
        try:
            completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=45,
                n=1,
                stop=None,
                temperature=0.5,
            )
            a_pred = completion.choices[0].text;
            print(a_pred)
        except openai.error.OpenAIError as e:
            print("An error occurred: {}".format(e))
            predictions, raw_outputs = self.question_classifier.predict([question])

            if predictions[0] == 0:
                self.tokenizer.encode_plus(question)
                encoding = self.tokenizer(question, context, return_tensors='pt', truncation=True,
                                          max_length=512)
                if len(encoding.input_ids) > 512:
                    print(encoding.input_ids)
                    encoding.input_ids = encoding.input_ids[:510]
                    encoding.attention_mask = encoding.attention_mask[:510]
                    encoding.token_type_ids = encoding.token_type_ids[:510]
                outputs = self.vqamodel(**encoding)
                answer_start_index = outputs.start_logits.argmax()
                answer_end_index = outputs.end_logits.argmax()
                predict_answer_tokens = encoding.input_ids[0, answer_start_index: answer_end_index + 1]
                answer_tokens_to_string = self.tokenizer.decode(predict_answer_tokens)
                a_pred = answer_tokens_to_string
                print('contextual')

            else:
                git_answer = generate_answers(vfeats, question)
                print(len(git_answer))
                a_pred = concatenate_strings(git_answer)  #git_answer[0] + git_answer[1]
                print('visual')

            if type(a_pred) != list:
                a_pred = a_pred.split('.')[0]
        print(a_pred)
        return a_pred

def concatenate_strings(strings):
    # Extract the right part after '?' of the first string
    string1 = strings[0][0]
    string2 = strings[1][0]
    string1_question_index = string1.find('? ')
    string1_right_part = string1[string1_question_index + 1:]

    # Extract the right part after '?' of the second string
    string2_question_index = string2.find('? ')
    string2_right_part = string2[string2_question_index + 1:]

    # Concatenate the two right parts with '/'
    concatenated_string = string1_right_part + '/' + string2_right_part

    return concatenated_string
