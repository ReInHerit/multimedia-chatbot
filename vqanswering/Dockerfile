FROM python:3.9-slim-buster

WORKDIR /webapp

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY package.json ./
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y npm
RUN npm install --force

COPY . .
EXPOSE $PORT
ARG OPENAI_KEY
ARG DJANGO_KEY
ENV OPENAI_KEY=$OPENAI_KEY
ENV DJANGO_KEY=$DJANGO_KEY
# to print Python output to console
ENV PYTHONUNBUFFERED=1

# run the server (local)
#ENTRYPOINT ["python", "manage.py"]
#CMD ["runserver", "0.0.0.0:8000"]
#for heroku
CMD gunicorn --bind 0.0.0.0:$PORT vqanswering.wsgi

