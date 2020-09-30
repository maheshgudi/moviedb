FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /moviedb

COPY . /moviedb

RUN apt update -y && apt upgrade -y

RUN pip install -r requirements.txt 

RUN python manage.py migrate && python manage.py upload_movies movie_file movies/imdb.json

CMD ["python", "manage.py", "runserver", "0.0.0.0:$PORT"]
