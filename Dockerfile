FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /moviedb

COPY . /moviedb

RUN apt update -y && apt upgrade -y

RUN pip install -r requirements.txt 

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
