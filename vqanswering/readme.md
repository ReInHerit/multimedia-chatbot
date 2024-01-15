# ReInHerit toolkit: VIOLA Multimedia ChatBot

**VIOLA** (**V**isual **I**ntelligence **O**n**L**ine **A**rt-assistant webapp) is a web application that uses visual content and text descriptions to provide AI assistance for artwork images. Through a chatbot, users can ask questions about the artwork and receive responses related to its visual or contextual aspects.</p> 
The user asks questions about the artwork and receives answers from a chatbot relating to the visual or contextual scope of the work. </p>
The web application follows a client-server architecture, with the client being the user interface created using HTML, CSS, and the jQuery framework, and the server being managed by the Django framework to handle database management and chatbot requests and responses. </p>
The user interface is divided into two sections: the home page and the gallery. The home page features a carousel of significant images and a button to access the gallery, where users can view all images in the database, filter them by name, and retrieve information about each artwork. Upon selecting an artwork, the user can access its file, which includes an enlarged image, and begin using the chatbot to ask questions about the artwork. </p>

<p>Download the repository and follow the instructions below to set up the application.</p>

---

## How to run the app
You can choose to test the app in two ways:
- creating a Python virtual environment
- using docker

Follow above pre-requisites and instructions paying attention to the parts relating to the chosen method.

### Pre-requisites
- **Python 3.9** installed on your machine. If you don't have it, you can download it from the official website: https://www.python.org/downloads/ or follow this online guide: https://realpython.com/installing-python/ to install Python on your machine.
- **Javascript** enabled on your browser. If not, you can follow this online guide: https://www.enable-javascript.com/
- a **Django secret key** and an **OpenAI API key** are required, **Google Analytics** is optional:\
You need to rename the file .env_template to .env and fill in the fields with your own key values:<br>
  1. ___Django secret key___: 
     1. To generate a Django secret key in the terminal, navigate to the "utils" folder and run the following command: 
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
      7. Download pytorch_model.bin and config.json from https://huggingface.co/Faisalrahi/pytorch_model.bin/tree/main and place it in the question_classifier/models/vqa_bert folder.
  3. ___Google Analytics key___
     1. Go to https://analytics.google.com/analytics/web/ and click on the "Get Started for Free" button.
     2. Sign in with your Google account.
     3. Follow the instructions to create a new account.
     4. Once you have created your account, you will be redirected to the dashboard. Click on the "Admin" button in the top left corner.
     5. Click on the "Create Property" button.
     6. Select "Web" as the property type and click on the "Continue" button.
     7. Enter a name for your property and click on the "Create" button.
     8. Click on the "Tracking Info" button.
     9. Click on the "Tracking Code" button.
     10. Copy the "Tracking ID" and paste it in the GA_KEY field of the .env file.
- Depending on which method you have chosen to test the app you must:
  - **Python Virtual Environment**: we recommend using Conda to manage virtual environments, so check in your terminal or command prompt if you have Conda installed by running the command 
    ```
    conda --version 
    ``` 
    If Conda is not installed, follow the installation instructions from the official Anaconda website: https://docs.anaconda.com/anaconda/install/
  - **Docker**: you'll need to set up and run Docker on your operating system. If you are not familiar with Docker, please refer to the official documentation [here](https://docs.docker.com/). 
 
    
### How to manage Python virtual environment
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

- ##### Create your Docker container image 
    To build the image using the Dockerfile, open a terminal, navigate to the folder containing the Dockerfile and type:  
    ```
    docker build -t chatbot .
    ```  
    The dot at the end specifies the current directory. \
    Replace my_webapp_name with a relevant name for your app. \
    If the build come out with an error, relaunch it until it is completed. 
    
    Be patient, it may take many minutes to finish the process.
- ##### Run your app container
    Now that you have an image, you can run the application in a container. To do so, you will use the docker run command.  
    ```
    docker run --env-file=.env -p 8000:8000 chatbot
    ``` 
    Remember to replace my_webapp_name with the one chosen in the build process.\
    When you start the container run it will take a few minutes to download the models and files necessary for the app to function. Be patient here too.

- #### Open the home page
    Now open a browser and go to the address:  
    ```
    localhost:8000
    ```
  
---
## ADMINISTRATOR GUIDE
### How to create a superuser
To set up a superuser for the Django admin, you can follow these steps:

- Open a terminal or command prompt.

- Navigate to your Django project's root directory where the manage.py file is located.

- Run the following command to create a superuser:
   ```
    python manage.py createsuperuser
   ```
- You will be prompted to enter a username. Type in the desired username for the superuser and press Enter.

- Next, you will be prompted to enter an email address. You can either provide a valid email address or leave it blank by pressing Enter.

- Lastly, you will be prompted to enter a password. Type in a secure password for the superuser. Note that the password won't be visible as you type for security reasons. Press Enter when done.

If the superuser is created successfully, you should see a message like:
   ```
    Superuser created successfully
   ```
That's it! You have now set up a superuser for the Django admin. You can use the provided username and password to log in to the admin interface and access administrative features.

To access the Django admin, run your Django development server:
   ```
   python manage.py runserver
   ```
and navigate to http://localhost:8000/admin/ 

Log in using the superuser credentials, and you will have full administrative access to manage your Django application.
### Manage Database
Clicking on **Artworks** you can see all the artworks in the database if they exist in the database.

You may filter the artworks by year or century or search the artworks with text.
Clicking on an Artwork's title you access to the change section of that artwork where you can modify the artwork's information.
#### Add new Artwork/s 
There are two methods to add a new artwork to the database:
1. **Add artwork manually from Admin Page**: \
Generate full and thumbnail images of the artwork and place them in the **static/assets/img/full** and **static/assets/img/thumbs** respectively.\
Log in to the admin page and navigate to **Artworks**. \
Click on either **Add** or **ADD ARTWORK** buttons and complete the form with the artwork's data: \
   - Fill the **image** and **thumb** fields with the respective paths (e.g., static/assets/img/full/my_image.jpg and static/assets/img/thumbs/my_image.jpg).
   - Ensure to provide a detailed description in the **Description** field for better accuracy in the chatbot.
   - The **Link** field will be automatically populated.


2. **Add artworks from a Folder**: \
Go to static/assets/add_new_files folder. Here you can save all the artworks images you want to add to the database following these rules:
   - Thumbnails are not required as the system generates them automatically.
   - Title the images with a meaningful name, preferably the artwork's title (replace spaces with underscores).
   - Create a .txt file in the same folder with the same name as the image. 
   - In the text file, provide: 
     - Description of the artwork with as many details as possible (You should write a complete description).
     - Additional information, each on a new line (put Unknown if you don't know):
       - **Date:** (e.g. around 420 BC) 
       - **Type of object:** (e.g. Pottery)
       - **Measurement:** (e.g. H. 28.8 cm)
       - **Maker:** (e.g. Leonardo da Vinci)
       - **Materials and techniques:** (e.g. Clay)
       - **Location:** (e.g. Museum of YourMuseum)
       - **Link:** (e.g. [https://address_of_the_artwork]) \
       
Example: \
       
       The painting depicts the Virgin Mary, the Christ Child, six angels, and various figures including apostles, prophets, and saints.
       Date: around 420 BC
       Type of object: Pottery
       Measurement: H. 28.8 cm
       Maker: Leonardo da Vinci
       Materials and techniques: Clay
       Location: Museum of YourMuseum
       Link: https://address_of_the_artwork
       
Once the folder is prepared, in the administrator page, click on **Artworks** and then on **Add artworks from folder**. The system will create the artworks in the database and move/create the images in the folders.

#### How to remove one (or some) artwork from the database:
Deleting an artwork from the database will remove all associated information, including images (full and thumb). Follow these steps in the admin page:
- Navigate to **Artworks**. \
- Check the box next to the artwork/s you wish to remove.
- Under Action select **Delete selected artworks** and click on the **GO** button.
- A new page will display the list of selected artworks. Confirm or cancel the operation.
- Click on **YES, I'M SURE** to confirm the operation.
---
## Chatbot
On the chatbot page, the user interface is split into two sections, the left-hand side of which displays the artwork's title, year, and image, while the right-hand side displays the chat interface. \
The user can utilize the chat interface to inquire about the artwork in question.

When the user submits a question, Django handles the request, and the ***handle_chat_question*** function in the views.py file sends a request to the ***produce_answer*** function of the ***AnswerGenerator*** class located in the answer_generator.py file.

The produce_answer function takes in the user's question, along with the artwork's title, year, context (which consists of both visual and contextual phrases from the artwork's card), and image URL as inputs. It then sends a prompt, which is a structured string, to the OpenAI GPT-3 API. The prompt is structured to inform the API about the artwork in question and to provide a template for the response.
```
prompt = "Provide a clear and concise answer in the same language as the question within 30 words. "
         "If the question is unrelated to the artwork, please state so. "
         "If the information is not available in the Context, indicate that you don't have the information, "
         "writing in the language of the question 'I don't have this information.' "
         "If there's difficulty understanding the question, ask the user to clarify the question. "
         "Never start your answer with 'Answer:' and never use names or information that are not in the 'Context'. "
         "If the question is in first person singular, respond in second person singular. "
         "I want you to act as an art expert and remember to answer in the same language of the question. "
         "If the translated answer is longer than the limit of 30 words, rephrase it to stay in that limit. "
         "If the Context is not enough to answer, respond with your internal knowledge, saying that the answer could be imprecise. "
```

The OpenAI GPT-3 API takes the prompt and searches for an answer within the context of the artwork provided. If the answer is found within the contextual phrases, it is reformulated to ensure that the response does not exceed 15 words. If the answer cannot be found within the contextual phrases, the API will return "I don't know" or "I don't have this information" as a response.

When the chatbot could not find an answer within the contextual phrases, it feeds a json file called **unresolved_question.json** in **static/assets/json** folder with the artwork's title and the unanswered question. This file could be usefull for museum curator to improve the description with the missing information.
```
---
