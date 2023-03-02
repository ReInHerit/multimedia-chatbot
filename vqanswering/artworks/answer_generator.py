from question_classifier.bert import get_pretrained_bert
import os
from transformers import DistilBertForQuestionAnswering, DistilBertTokenizer
import torch
from google_trans_new import google_translator
from .git_vqa import generate_answers
import openai
import json
from dotenv import load_dotenv


os.environ['CUDA_VISIBLE_DEVICES'] = '0'
# OPEN-AI APIs
load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')
# Set up the model
model_engine = "text-davinci-003"
# WHICH TO USE
json_which = open('./static/assets/json/which_to_use.json')
which_data = json.load(json_which)
which = which_data['using']

device = "cuda" if torch.cuda.is_available() else "cpu"


class AnswerGenerator:
    def __init__(self):
        super(AnswerGenerator, self).__init__()

        self.question_classifier = get_pretrained_bert(use_cuda=False)
        self.translator = google_translator()

        model_name = 'distilbert-base-uncased'

        self.vqa_model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_name,
                                                             return_token_type_ids=True)
        self.vqa_model.eval()

    def produce_answer(self, question, artwork_title, year, context, image_url):
        print(question)
        if which == 'open_ai':
            # prompt contextual
            prompt = f"Consider the painting {artwork_title}  depicted in {year}. {question}" \
                     f"Answer truthfully using the Context as source of information and with up to 15 words. " \
                     f"If the answer is not contained in the Context, provide accurate information on the painting. " \
                     f"If the question is not relevant to the painting, kindly state so. " \
                     f"If the question is relevant but you don't have a relevant answer, state that you don't have the information. " \
                     f"Context: {context}."
            print(prompt)

            # Generate a response openAi
            try:
                completion = openai.Completion.create(
                    engine=model_engine,
                    prompt=prompt,
                    max_tokens=25,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                answer = completion.choices[0].text
            except openai.error.OpenAIError as e:
                print("An error occurred: {}".format(e))
                # try: bert and git
                answer = self.use_cqa_or_vqa(question, context, image_url)
        else:
            answer = self.use_cqa_or_vqa(question, context, image_url)
        print('A: ', answer)
        return answer
    
    def use_cqa_or_vqa(self, question, context, url):
        predictions, raw_outputs = self.question_classifier.predict([question])
    
        if predictions[0] == 0:
            self.tokenizer.encode_plus(question)
            encoding = self.tokenizer(question, context, return_tensors='pt', truncation=True, max_length=512)
    
            if len(encoding.input_ids) > 512:
                encoding.input_ids = encoding.input_ids[:510]
                encoding.attention_mask = encoding.attention_mask[:510]
                encoding.token_type_ids = encoding.token_type_ids[:510]
            outputs = self.vqa_model(**encoding)
            answer_start_index = outputs.start_logits.argmax()
            answer_end_index = outputs.end_logits.argmax()
            predict_answer_tokens = encoding.input_ids[0, answer_start_index: answer_end_index + 1]
            answer_tokens_to_string = self.tokenizer.decode(predict_answer_tokens)
            answer_prediction = answer_tokens_to_string
            print('contextual')
    
        else:
            git_answer = generate_answers(url, question)
            answer_prediction = concatenate_strings(git_answer)
            print('visual')
    
        if type(answer_prediction) != list:
            answer_prediction = answer_prediction.split('.')[0]
        return answer_prediction
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

