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
model_engine = "gpt-3.5-turbo" #"text-davinci-003"


class AnswerGenerator:
    def __init__(self):
        super(AnswerGenerator, self).__init__()

    def produce_answer(self, question, artwork_title, context):
        print(question)
        # if which == 'open_ai':
        print('using open ai')
        prompt = f"Consider the artwork titled '{artwork_title}' and its context. " \
                 f"Context: {context}. \n" \
                 f"Question: {question}. \n" \
                 f"Provide a clear and concise answer using the same language as the question within 30 words." \
                 f"If the question is unrelated to the artwork, please state so. \n" \
                 f"If the information is not available in the context, indicate that or write in the language of the question 'I don't have this information.'.\n " \
                 f"If there's difficulty understanding the question, request clarification. \n" \
                 f"Never start your answer with 'Answer:' and never use names or information that are not in the 'Context'.\n" \
                 f"If the question is in first person singular, respond in second person singular.\n" \
                 f"I want you to act as an art expert and remember to answer in the same language of the question. \n " \
                 f"If the translated answer is longer than the limit of 30 words, rephrase it to stay in that limit.\n" \
                 f"Answer:"
        # prompt

        print(prompt)

        retry_count = 0
        max_retries = 3
        retry_delay = 1  # seconds

        while retry_count < max_retries:
            try:
                completion = openai.Completion.create(
                    engine=model_engine,
                    prompt=prompt,
                    max_tokens=80,
                    n=1,
                    stop=None,
                    temperature=0.2,
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
