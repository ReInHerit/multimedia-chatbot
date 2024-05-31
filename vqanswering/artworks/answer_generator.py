import ast
import base64
import os
import re
import time

import openai
import json

import string
from dotenv import load_dotenv
from langdetect import detect
from .models import Artwork, Chat

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
# OPEN-AI APIs
load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')
# Set up the model
model_engine = "gpt-4o-2024-05-13"  # "gpt-4-0125-preview""text-davinci-003""gpt-4"gpt-3.5-turbo-1106  gpt-3.5-turbo-0125


# i_dont_know_answer = ["I don't have this information",
#                       "The context does not provide any",
#                       "The context provided does not",
#                       "not specified in the provided",
#                       "there is no information"]
#
# i_dont_know_any_language = {
#     "English": [
#         "I don't have this information",
#         "The context does not provide any",
#         "The context provided does not",
#         "not specified in the provided",
#         "there is no information"
#     ],
#     "Italian": [
#         "Non ho queste informazioni",
#         "Il contesto non fornisce alcuna informazione",
#         "Il contesto fornito non fornisce",
#         "non specificato nel fornito",
#         "non c'è alcuna informazione"
#     ],
#     "French": [
#         "Je n'ai pas cette information",
#         "Le contexte ne fournit aucune information",
#         "Le contexte fourni ne fournit pas",
#         "non spécifié dans le fourni",
#         "il n'y a pas d'information"
#     ],
#     "German": [
#         "Ich habe diese Informationen nicht",
#         "Der Kontext liefert keine Informationen",
#         "Der bereitgestellte Kontext liefert nicht",
#         "nicht im bereitgestellten spezifiziert",
#         "es gibt keine Informationen"
#     ],
#     "Greek": [
#         "Δεν έχω αυτές τις πληροφορίες",
#         "Ο περιβάλλοντας χώρος δεν παρέχει καμία πληροφορία",
#         "Ο παρεχόμενος περιβάλλοντας χώρος δεν παρέχει",
#         "δεν προσδιορίζεται στο παρεχόμενο",
#         "δεν υπάρχουν πληροφορίες"
#     ]
# }


def load_i_dont_know_any_language():
    with open("static/assets/json/i_dont_know_any_language.json", "r", encoding='utf-8') as json_file:
        i_dont_know_any_language = json.load(json_file)
    return i_dont_know_any_language


def load_json_file(file):
    with open(file, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


i_dont_know_any_language = load_json_file("static/assets/json/i_dont_know_any_language.json")
languages = load_json_file("static/assets/json/languages.json")


class AnswerGenerator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AnswerGenerator, cls).__new__(cls)
            cls._instance.last_question = ""
            cls._instance.last_answer = ""
            cls._instance.last_artwork_title = ""
            cls._instance.unresolved_questions = {}
            cls._instance.solved_questions = {}
            cls._instance.load_existing_data()
        return cls._instance

    def load_existing_data(self):
        if os.path.exists("static/assets/json/qa_pairs.json"):
            with open("static/assets/json/qa_pairs.json", "r", encoding='utf-8') as json_file:
                self.solved_questions = json.load(json_file)
        if os.path.exists("static/assets/json/unresolved_questions.json"):
            with open("static/assets/json/unresolved_questions.json", "r", encoding='utf-8') as json_file:
                self.unresolved_questions = json.load(json_file)

    def save_data(self):
        with open("static/assets/json/qa_pairs.json", "w", encoding='utf-8') as json_file:
            json.dump(self.solved_questions, json_file, indent=2, ensure_ascii=False)
        with open("static/assets/json/unresolved_questions.json", "w", encoding='utf-8') as json_file:
            json.dump(self.unresolved_questions, json_file, indent=2, ensure_ascii=False)

    def produce_answer(self, question, language, artwork):
        context = (artwork.description + " year: " + str(artwork.year) + " subject: " + artwork.subject +
                   " type of object: " + artwork.type_of_object +
                   " materials and techniques: " + artwork.materials_and_techniques +
                   " measurament: " + artwork.measurement + " maker: " + artwork.maker)
        title = artwork.title
        image_path = artwork.thumb_image
        if title != self.last_artwork_title:
            # Reset last_question and last_answer if artwork_title has changed
            self.last_question = ""
            self.last_answer = ""
            print('resetted last question and last answer')
        self.last_artwork_title = title
        base64_image = encode_image(image_path)
        system_prompt = (
            "Follow these steps to answer the user question: "
            "Step 1: Read the question carefully, understand it and remember the language it has been written. "
            "Step 2: Provide a clear answer keeping in mind the following guidelines: "
            "- Answer in the same language as the question. "
            "- Answer within 30 words "
            "- If the question is unrelated to the artwork, please state so. "
            "- If there's difficulty understanding the question or if the question is not comprehensible, "
            "explicitly state that and ask the user to reformulate the question. Use one of these responses: "
            "'I'm sorry, I didn't understand the question. Could you please reformulate it?' "
            "'I didn't catch that. Could you clarify your question?' "
            "'Your question is not clear to me. Could you please rephrase?' "            
            "- If the information is not available in the context, try your best to generate an answer based on the "
            "available information. If you can't provide an answer, then you can randomly use one of these possible "
            "responses: "
            "'I'm sorry, but I don't have that information in the context provided.' "
            "'I apologize, but I can't find that information in the details I have.' "
            "'Sorry, I don't have those details in the given context.' "
            "'I'm afraid that information isn't available in the context I have.' "
            "'I can't find this information in the artwork's details.' "
            "and suggest the user to ask something else. "
            "- Never start your answer with 'Answer:' and never use names or information that are not in the 'Context'. "
            "- If the question is in first person singular, respond in second person singular. "
            "Step 3: Translate the produced answer in the same language of the question. "
            "Step 4: Provide the answer to the user in JSON format with the following keys: question, question language, answer, answer translated, resolved, understood. "
            "Step 5: The JSON format should be: "
            '{'
            '"question": "The original question", '
            '"question language": "The language of the question", '
            '"answer": "The concise answer", '
            '"answer translated": "The translated answer", '
            '"resolved": "True if answered with context informations, False if not (unresolved)", '
            '"understood": "True if question is understood, False if not understood"'
            '}'
        )
        prompt = (f"You are an assistant for question-answering tasks. Consider the artwork titled '{title}' "
                  f"and use the following pieces of retrieved Context to answer the question "
                 f"Context: {context}. \n"
                 f"Question: {question}. \n"
                 f"Answer:"
                  )
        if self.last_question != "" and self.last_answer != "":
            system_prompt += (f" - If the current question is the same as the last question, generate a different "
                              f"response to avoid repetition. Last Q: {self.last_question} Last A: {self.last_answer} \n")
        print(language)

        retry_count = 0
        max_retries = 3
        retry_delay = 1  # seconds
        while retry_count < max_retries:
            try:
                completion = openai.ChatCompletion.create(
                    model=model_engine,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"}
                             }
                        ]},
                    ],
                    temperature=0.25,
                )
                # choices = completion.choices
                answer = completion.choices[0].message["content"]
                chat = analyze_answer(answer, question, language, artwork)

                self.last_question = question
                self.last_answer = chat.answer

                self.save_data()
                break  # Break the loop if the API call is successful
            except openai.error.OpenAIError as e:
                print("An error occurred: {}".format(e))
                self.last_answer = "There's a problem with the OpenAI API, please try again later"

            retry_count += 1
            print("Retrying in {} second(s)...".format(retry_delay))
            time.sleep(retry_delay)

        print('answer', chat.answer)
        return self.last_answer


def encode_image(image_path):
    print(image_path)
    base_dir = os.path.dirname(__file__)
    print(base_dir)  # get the directory of the current script
    full_path = os.path.join(base_dir, '..', image_path.lstrip('/'))  # construct the full path
    print(full_path)
    with open(full_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def is_english(text):
    try:
        lang = detect(text)
        return lang == 'en'
    except:
        # If langdetect encounters an error (e.g., short input), return False
        return False


def find_lang(text):
    try:
        print(text)
        lang = detect(text)
        print(lang)
        if lang.startswith('zh'):
            lang_name = 'Chinese'
        else:
            for language in languages:
                print(languages[language][0])
                if languages[language][0].startswith(lang):

                    lang_name = language
                    return lang_name
                else:
                    lang_name = 'English (United Kingdom)'

        return lang_name
    except:
        # If langdetect encounters an error (e.g., short input), return False
        return False


def extract_json(answer):
    # Check if the answer contains JSON content
    if "{" in answer:
        start_index = answer.index("{")
        end_index = answer.rindex("}") + 1
        json_part = answer[start_index:end_index]
        json_part = json_part.replace(': True', ': true').replace(': False', ': false')
        print('Answer:', answer)
        print('JSON content found:', repr(json_part))
        try:
            return json.loads(json_part)
        except json.JSONDecodeError as e:
            print('Invalid JSON content:', json_part)
            print('Error:', repr(e))
            return None
    else:
        return None


def handle_keyword_responses(answer, question, language):
    # Check if the answer starts with any predefined keywords
    for keyword in i_dont_know_any_language:
        for phrase in i_dont_know_any_language[keyword]:
            if answer.startswith(phrase):
                print("No information available for:", answer)
                q_lan = find_lang(question)
                print(q_lan)
                translated_answer = i_dont_know_any_language[q_lan][0] if q_lan else \
                    i_dont_know_any_language['English (United Kingdom)'][0]

                return {
                    "answer": translated_answer,
                    "question": question,
                    "question language": "English (United Kingdom)" if is_english(question) else language,
                    "answer translated": translated_answer
                }
    return None


def analyze_answer(answer, question, language, artwork):
    # Extract JSON content
    json_dict = extract_json(answer)
    if json_dict:
        if check_existing_qa(artwork, question, json_dict['answer'], json_dict['resolved']):
            print('Similar Q&A already exists in the database.')
            return None
        else:
            chat = Chat.objects.create(
                artwork=artwork,
                question=question,
                answer=json_dict['answer'],
                question_language=json_dict['question language'],
                resolved=json_dict['resolved']
            )
            return chat

    print('Handle keyword-based responses')
    keyword_response = handle_keyword_responses(answer, question, language)
    if keyword_response:
        if check_existing_qa(artwork, question, keyword_response['answer'], False):
            print('Similar Q&A already exists in the database.')
            return None
        else:
            chat = Chat.objects.create(
                artwork=artwork,
                question=question,
                answer=keyword_response['answer'],
                question_language=keyword_response['question language'],
                resolved=False
            )
            return chat

    print(' Default case: No JSON content or keyword match')
    translated_answer = answer if is_english(question) else i_dont_know_any_language.get(language, [answer])[0]
    if check_existing_qa(artwork, question, translated_answer, True):
        print('Similar Q&A already exists in the database.')
        return None
    else:
        chat = Chat.objects.create(
            artwork=artwork,
            question=question,
            answer=translated_answer,
            question_language="English (United Kingdom)" if is_english(question) else language,
            resolved=True
        )
        return chat


def check_existing_qa(artwork, question, answer, resolved):
    existing_chat = Chat.objects.filter(
        artwork=artwork,
        question=question,
        answer=answer,
        resolved=resolved
    )
    return existing_chat.exists()