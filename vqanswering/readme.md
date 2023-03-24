# reinHerit toolkits: VIOLA Multimedia ChatBot
## Description of the web app
**VIOLA** (**V**isual **I**ntelligence **O**n**L**ine **A**rt-assistant webapp) is a web application that uses visual content and text descriptions to provide AI assistance for artwork images. Through a chatbot, users can ask questions about the artwork and receive responses related to its visual or contextual aspects.</p> 
The user asks questions about the artwork and receives answers from a chatbot relating to the visual or contextual scope of the work. </p>
The web application follows a client-server architecture, with the client being the user interface created using HTML, CSS, and the jQuery framework, and the server being managed by the Django framework to handle database management and chatbot requests and responses. </p>
The user interface is divided into two sections: the home page and the gallery. The home page features a carousel of three significant images and a button to access the gallery, where users can view all images in the database, filter them by century, and retrieve information about each artwork. Upon selecting an artwork, the user can access its file, which includes an enlarged image, and begin using the chatbot to ask questions about the artwork. </p>

<p>Download the repository and follow the instructions below to set up the application.</p>

---

## How to run the app
You can choose to test the app in two ways:
- creating a python virtual environment
- using docker

Follow above prerequisites and instructions paying attention to the parts relating to the chosen method.

### Prerequisites
- **Python 3.9** installed on your machine. If you don't have it, you can download it from the official website: https://www.python.org/downloads/ or follow this online guide: https://realpython.com/installing-python/ to install Python on your machine.
- **Javascript** enabled on your browser. If not, you can follow this online guide: https://www.enable-javascript.com/
- a **Django secret key** and an **OpenAI API key** are required:\
You need to rename the file .env_template to .env and fill in the fields with your own key values:<br>
  1. ___Django secret key___: 
     1. You can generate one by typing in a terminal 
        >   python getYourDjangoKey.py 

     2. copy and paste the generated key in the DJANGO_KEY field of the .env file. Don't forget to put it in quotation marks.

     <br>
  2. ___openAI API key___: Follow these simple steps to create your OpenAI API key:
      1. Go to https://platform.openai.com/signup to create a free account.
      2. View pricing details here: https://openai.com/pricing
         - for best results we are using InstructGPT Davinci, which is currently $0.0200/1K tokens, which are about 750 words.
      3. Add your credit card. In OpenAI > Click your user logo > Manage Account > Billing. Then follow the prompts.
         - Also, set limits, so you don't exceed your desired limit, they default to ~$120. Settings are under Billing > Usage Limits
      4. Access your OpenAI key page by visiting https://platform.openai.com/account/api-keys.
      5. Click the "Create new secret key" button on the key page to generate a new key.
      6. Copy the key and paste it in the OPENAI_KEY field of the .env file. Don't forget to put it in quotation marks.
      7. Download pytorch_model.bin from https://huggingface.co/Faisalrahi/pytorch_model.bin/blob/main/pytorch_model.bin and place it in the question_classifier/models/vqa_bert folder.
- Depending on which method you have chosen to test the app you must:
  - **Python Virtual Environment**: we recommend using Conda to manage virtual environments, so check in your terminal or command prompt if you have Conda installed by running the command 
    ```
    conda --version 
    ``` 
    If Conda is not installed, follow the installation instructions from the official Anaconda website: https://docs.anaconda.com/anaconda/install/
  - **Docker**: you'll need to set up and run Docker on your operating system. If you are not familiar with Docker, please refer to the official documentation [here](https://docs.docker.com/). 
### How to switch between openAI GPT-3 and Bert & GIT Methods
If you want to test the app using both methods, you can switch between them. Before proceeding, you'll need to modify the value of the 'using' variable in the 'which_to_use.json' file located in 'static/assets/json'..

```
{
  "using": "open_ai"
}
```
If you want to use the openAI GPT-3 method, set the value to **open_ai**.\
If you want to use the Bert & GIT method, set the value to anything other than **open_ai**.
### How to manage python virtual environment
- #### Create a virtual environment and install the requirements
    Open a terminal and navigate to the folder containing the requirements.txt file. \
    Create a virtual environment by typing: 
    ```
    conda create --name my_env_name python=3.9
    ```
    Activate the environment by typing:
    ``` 
    conda activate my_env_name
    ```
    <p>Notice: Replace my_env_name with a relevant name for your environment.
    <p>You have successfully activated your virtual environment. To install the Python libraries required for your project, run the following command while inside the virtual environment: 
    
    ``` 
    pip install -r requirements.txt
    ``` 
    
- #### How to run the server
  Open a terminal and navigate to the folder containing the manage.py file. It should be the same as requirement.txt\
  Type:
  ```
  python manage.py runserver
  ```
- #### Open the home page
    Now open a browser and go to the address:  
    ```
    localhost:8000/home
    ```

### How to manage docker
Once ready with the .env file you can create and launch the docker image.

- ##### Create your docker container image 
    To build the image using the Dockerfile, open a terminal, navigate to the folder containing the Dockerfile and type:  
    ```
    docker build -t my_webapp_name .
    ```  
    The dot at the end specifies the current directory. \
    Replace my_webapp_name with a relevant name for your app. \
    If the build come out with an error, relaunch it until it is completed. 
    
    Be patient, it may take many minutes to finish the process.
- ##### Run your app container
    Now that you have an image, you can run the application in a container. To do so, you will use the docker run command.  
    ```
    docker run --env-file=.env -p 8000:8000 my_webapp_name
    ``` 
    Remember to replace my_webapp_name with the one chosen in the build process.\
    When you start the container run it will take a few minutes to download the models and files necessary for the app to function. Be patient here too.

- #### Open the home page
    Now open a browser and go to the address:  
    ```
    localhost:8000/home
    ```
  
---

## Database
The database is created starting from a json file which contains the data of each artwork.\
The basic model of a card is as follows:
```
"1 (the numeric id of the artwork)": {
 "title": "title of the artwork",
 "img_url": "path or url to the image",
 "year": 1970,
 "visual_sentences": [
   "A list of sentences describing the visual aspect of the artwork",
   "The more detailed your list, the better the answer you will receive."
 ],
 "contextual_sentences": [
   "A list of sentences describing the contextual aspect of the artwork",
   "The more you put here better answer you receive."
 ],
 "split": "you can use this parameter to find if the schedule is present (ADDED) or not (TRAIN) in the database"
}
```
To import the works into the system, we provide a JSON file containing all the card information as input to the import_datas() function in the import_datas.py file. This function transfers the data into Artwork objects, which are used by the system to provide information to the chatbot and user interface as needed.

### How to replace the actual database with your own artworks
[Only for the python virtual environment method!]
<p>You need to:

- Create a new json file with the same structure as the **rehineritpedia.json** file in the _static/assets/json_ folder.
- Edit the content with your artworks datas, remember to fill in the "visual_sentences" and "contextual_sentences" fields with as many descriptive sentences as possible, the more you enter the more accurate the chatbot will be.
- Replace the rehineritpedia.json file with the new one.
- In the **artworks/views.py** file, uncomment lines 20, 23 and 24 (incidentally those under the comments **# TO DELETE ALL ARTWORKS** and **# TO ADD ARTWORK/s**)
- Save the file and either refresh **localhost:8000/home** if the server is already running or follow the instructions on _[how to run the server](#how-to-run-the-server)_.
- Navigate to gallery and wait till is loaded.
- To prevent adding the artworks more than once, comment above lines in the "artworks/views.py" file and save again.
- Refresh localhost:8000/home and navigate to gallery. Everything should be ok. 

### How to add some artworks to the database:
- Duplicate and rename the **rehineritpedia.json** file in the _static/assets/json_ folder with a name of your choice.
- Delete the old entries in the **rehineritpedia.json** file and fill it with the data of only the new paintings you want to add.
- In the **artworks/views.py** file, uncomment lines 23 and 24 (beneath **# TO ADD ARTWORK/s** comment)
- Save the file and either refresh **localhost:8000/home** if the server is already running or follow the instructions on _[how to run the server](#how-to-run-the-server)_.
- Navigate to gallery and wait till is loaded.
- To prevent adding the artworks more than once, comment above lines in the "artworks/views.py" file and save again.
- Refresh localhost:8000/home and navigate to gallery. Everything should be ok. 

### How to remove one (or some) artwork from the database:
- In the "artworks/views.py" file, uncomment line 17 and enter the URL of the artwork to be removed in the "image" option.
- To remove multiple artworks at once, duplicate the line and give each variable a unique name, such as "delete_artwork1", "delete_artwork2", etc.
- Save the file.
- If the server is running, refresh "localhost:8000/home" and then click on "enter gallery". If not, follow the instructions on _[how to run the server](#how-to-run-the-server)_ and then click on "enter gallery".
- To prevent adding the artworks more than once, comment above line/s in the "artworks/views.py" file and save again.
- Refresh localhost:8000/home and navigate to gallery. Everything should be ok. 
---
## Chatbot
On the chatbot page, the user interface is split into two sections, the left-hand side of which displays the artwork's title, year, and image, while the right-hand side displays the chat interface. \
The user can utilize the chat interface to inquire about the artwork in question.

When the user submits a question, Django handles the request, and the ***handle_chat_question*** function in the views.py file sends a request to the ***produce_answer*** function of the ***AnswerGenerator*** class located in the answer_generator.py file.

The produce_answer function takes in the user's question, along with the artwork's title, year, context (which consists of both visual and contextual phrases from the artwork's card), and image URL as inputs. It then sends a prompt, which is a structured string, to the OpenAI GPT-3 API. The prompt is structured to inform the API about the artwork in question and to provide a template for the response.
```
prompt = f"Consider the painting {artwork_title} depicted in {year}. {question}" \
         f"Answer truthfully using the Context as source of information and with up to 15 words. " \
         f"If the answer is not contained in the Context, provide accurate information on the painting. " \
         f"If the question is not relevant to the painting, kindly state so. " \
         f"If the question is relevant but you don't have a relevant answer, state that you don't have the information. " \
         f"Context: {context}."
```

The OpenAI GPT-3 API takes the prompt and searches for an answer within the context of the artwork provided. If the answer is found within the contextual phrases, it is reformulated to ensure that the response does not exceed 15 words. If the answer cannot be found within the contextual phrases, the API will return "I don't know" as a response.

In the event that there is a problem with the API query, such as a network issue, the system will pass the user's question to **BERT**, which is responsible for determining whether the question is visual or contextual. 
- If the question is contextual, BERT attempts to provide an answer using the sentences contained in the corresponding artwork card. 
- If the question is visual in nature, the chatbot server sends the question and image to **GIT**, an image analysis tool. GIT analyzes the image and attempts to generate a response to the user's question.
---
## To-Do
- [ ] Currently, there is a delay in loading artworks when the user navigates to the gallery page. This is due to the page evaluating each artwork's image and retrieving its thumbnail online. 
  - To address this issue, we could consider implementing a loading bar or a similar feature. Alternatively, we could revise the logic and store the images on the server side instead of relying on internet links.
- [ ] The selected artwork page is poor of content. Currently, it's just a pass-through page for the chatbot. It only contains the title, year, and image of the artwork, and a link to the chatbot below it. 
  - We could either integrate the chatbot directly into this page or add a textual description of the artwork, for example, using the contextual and visual phrases in the database's JSON file.
  - We could also add a link to the artwork's Wikipedia page, if it exists.
  - We could also add a link to the artwork's source, if it exists.
  - We could also add a link to the artist's Wikipedia page, if it exists.
- [ ] We have to find tune the chatbot answer. 
  1. The chatbot is currently limited to 15 words, so sometimes it responds with a truncated answer. 
     - We could consider increasing the word limit to 30 or 50 words.
     - We could also consider adding a "read more" button to the chatbot response, which would open a modal with the full answer.
  2. The chatbot sometimes responds with empty answers:
     - We need to write a better prompt that manage also this case.
  3. The user can write his question in a language different from English, but the answer is always in English:
     - We need to write in the prompt to translate tha answer in the same language of the question.
  4. The chatbot answers to questions do not take into account previous questions/answers, which generates issues such as:
        > Q1: Who do we see depicted in the painting?
      
        > A1: The painting depicts the Virgin Mary, the Christ Child, six angels, and various figures including apostles, prophets, and saints.
  
        > Q2: Who do we see on the sides of the painting?
  
        > A2: The six angels holding the ornate throne are seen on the sides of the painting.
        
        > Q3: What are their names? 
  
        > A3: The painting depicts the Virgin Mary and the Christ Child. 
     
     **[WRONG ANSWER]**  
        The user is asking for the names of the angels, but the chatbot responds with the names of the main figures depicted in the painting, instead of answering with "I don't know".
        - We need to write in the prompt to take into account previous questions/answers.