FROM python:3.7.12-slim-buster

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN mkdir /dognet

WORKDIR dognet

COPY ./dognet .

CMD [ "python" , "manage.py", "runserver" , "0.0.0.0:8000"]
