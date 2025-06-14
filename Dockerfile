FROM python:3.12-slim

RUN mkdir /app
WORKDIR /app

ADD requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD src /app/src