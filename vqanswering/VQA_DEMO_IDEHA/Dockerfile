FROM python:3.7-slim-buster

# Set the working directory to /app
WORKDIR /vqa_app

# Copy the current directory contents into the container at /app
ADD . /vqa_app

RUN apt-get update -y

# gcc compiler and opencv prerequisites
RUN apt-get -y install nano git build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1-mesa-glx ffmpeg libsm6 libxext6

# Detectron2 prerequisites
RUN pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install cython
RUN pip install --user 'git+https://github.com/facebookresearch/fvcore'

# Detectron2 - CPU copy
RUN git clone https://github.com/facebookresearch/detectron2 detectron2_repo

RUN pip install --user -e detectron2_repo

RUN python -m pip install 'git+https://github.com/facebookresearch/detectron2.git@ffff8ac'

# Development packages
RUN pip install flask flask-cors requests opencv-python

RUN pip install Flask

RUN pip install -U WTForms

RUN pip install Flask-WTF

RUN pip install simpletransformers==0.7.0

RUN pip install Pillow

RUN pip install pandas

RUN pip install transformers==2.1.1

RUN pip install --user -U nltk

RUN pip install tensorboardX

ADD . /vqa_app
# Make port 80 available to the world outside this container
EXPOSE 80

CMD ["python", "vqa_app.py"]