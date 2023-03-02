FROM python:3.9

WORKDIR /webapp
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN #pip install tensorboardX
RUN pip install --upgrade simpletransformers

COPY package.json ./
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y npm
RUN npm install --force

COPY . .
EXPOSE 8000
ARG OPENAI_KEY
ARG DJANGO_KEY
ENV OPENAI_KEY=$OPENAI_KEY
ENV DJANGO_KEY=$DJANGO_KEY

# run the server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]


