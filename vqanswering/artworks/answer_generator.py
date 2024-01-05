import ast
import os
import time

import openai
import json

import requests
from dotenv import load_dotenv

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
# OPEN-AI APIs
load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')
# Set up the model
model_engine = "gpt-3.5-turbo"  # "text-davinci-003""gpt-4"gpt-3.5-turbo-1106
i_dont_know_answer = ["I don't have this information",
                      "The context does not provide any",
                      "The context provided does not",
                      "not specified in the provided"]

class AnswerGenerator:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AnswerGenerator, cls).__new__(cls)
            cls._instance.last_question = ""
            cls._instance.last_answer = ""
            cls._instance.last_artwork_title = ""
            cls._instance.unresolved_questions = {}
        return cls._instance

    def produce_answer(self, question, artwork_title, context):
        if artwork_title != self.last_artwork_title:
            # Reset last_question and last_answer if artwork_title has changed
            self.last_question = ""
            self.last_answer = ""
            print('resetted last question and last answer')

        self.last_artwork_title = artwork_title

        prompt = f"Consider the artwork titled '{artwork_title}' and its Context. " \
                 f"Context: {context}. \n" \
                 f"Question: {question}. \n" \
                 f"Answer:"
        system_prompt = (
            "Provide a clear and concise answer in the same language as the question within 30 words. "
            "If the question is unrelated to the artwork, please state so. "
            "If the information is not available in the Context, indicate that you don't have the information, "
            "writing in the language of the question 'I don't have this information.' "
            "If there's difficulty understanding the question, ask the user to clarify the question. "
            "Never start your answer with 'Answer:' and never use names or information that are not in the 'Context'. "
            "If the question is in first person singular, respond in second person singular. "
            "I want you to act as an art expert and remember to answer in the same language of the question. "
            "If the translated answer is longer than the limit of 30 words, rephrase it to stay in that limit. "
            "If the Context is not enough to answer, respond with your internal knowledge, saying that the answer could be imprecise. "
            # "Produce a json with the question and answer message and a boolean value that says if you can find the information in the context or not (true or false). "
            # 'Here is an example of the output expected: {"question": "", "answer": "", "result_found": true}'
        )
        if self.last_question != "" and self.last_answer != "":
            system_prompt += f"if they exist, take in account also the last question and answer: Q: {self.last_question} A: {self.last_answer} \n"

        print(prompt, "\n", system_prompt)
        answer = ""
        retry_count = 0
        max_retries = 3
        retry_delay = 1  # seconds
        while retry_count < max_retries:
            try:
                completion = openai.ChatCompletion.create(
                    model=model_engine,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.25,
                )
                answer = completion.choices[0].message["content"]
                result_found = True
                if any(keyword in answer for keyword in i_dont_know_answer):
                    result_found = False
                if not result_found:
                    if artwork_title not in self.unresolved_questions:
                        self.unresolved_questions[artwork_title] = {"unresolved": []}

                    self.unresolved_questions[artwork_title]["unresolved"].append(question)
                    with open("static/assets/json/unresolved_questions.json", "w") as json_file:
                        json.dump(self.unresolved_questions, json_file, indent=2)

                self.last_question = question
                self.last_answer = answer
                break  # Break the loop if the API call is successful
            except openai.error.OpenAIError as e:
                print("An error occurred: {}".format(e))
                answer = "There's a problem with the OpenAI API, please try again later"

            retry_count += 1
            print("Retrying in {} second(s)...".format(retry_delay))
            time.sleep(retry_delay)
        print(answer)
        return answer
