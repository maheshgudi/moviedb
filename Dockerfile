FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /moviedb

COPY . /moviedb

RUN apt update -y && apt upgrade -y &&	apt install postgresql-11 -y && apt install libpq-dev -y

RUN pip install -r requirements.txt 

