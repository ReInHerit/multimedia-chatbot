import os
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


class AnswerGenerator:
    def __init__(self):
        super(AnswerGenerator, self).__init__()

    def produce_answer(self, question, artwork_title, year, context, image_url):
        print(question)
        # if which == 'open_ai':
        print('using open ai')
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
                max_tokens=40,
                n=1,
                stop=None,
                temperature=0.5,
            )
            answer = completion.choices[0].text
        except openai.error.TimeoutError:
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
        finally:
            # Code to execute regardless of whether an exception was raised or not
            print("Completed the request to OpenAI API")

        print(f"Answer: {answer}")
        return answer
    
