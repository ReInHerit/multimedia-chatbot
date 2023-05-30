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
model_engine = "text-davinci-003"


class AnswerGenerator:
    def __init__(self):
        super(AnswerGenerator, self).__init__()

    def produce_answer(self, question, artwork_title, context):
        print(question)
        # if which == 'open_ai':
        print('using open ai')
        # prompt contextual
        prompt = f"Consider the painting {artwork_title} and its following context. " \
                 f"Provide a complete and truthful answer using the Context as a source of information within 25 words. " \
                 f"If the answer is contained in the Context, provide accurate information on the painting. " \
                 f"If the question is not relevant to the painting, kindly state so. " \
                 f"If the question is relevant but you don't have a relevant answer, state that you don't have the information. " \
                 f"If you don't understand the question due to errors in the orthography or bad English, " \
                 f"state that you don't understand and kindly ask to rewrite the question. \n" \
                 f"Never start your answer with: 'Answer:' and never use names or information that are not in the 'Context'.\n" \
                 f"Question: {question}. \n" \
                 f"Context: {context}." \
                 f"Answer:"
        print(prompt)

        retry_count = 0
        max_retries = 3
        retry_delay = 1  # seconds

        while retry_count < max_retries:
            try:
                completion = openai.Completion.create(
                    engine=model_engine,
                    prompt=prompt,
                    max_tokens=40,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                answer = completion.choices[0].text
                break  # Break the loop if the API call is successful
            except requests.Timeout:
                print("The request to OpenAI API has timed out")
                answer = "There was a timeout error, please try again later"
            except openai.error.APIError as e:
                print("An error occurred: {}".format(e))
                answer = "There's a problem with the OpenAI API, please try again later"
            except openai.error.OpenAIError as e:
                print("An error occurred: {}".format(e))
                answer = "There's a connection problem, please ask the question later"
            except Exception as e:
                print("An unexpected error occurred: {}".format(e))
                answer = "An unexpected error occurred, please try again later"

            retry_count += 1
            print("Retrying in {} second(s)...".format(retry_delay))
            time.sleep(retry_delay)

        print(answer)
        return answer
