FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

ADD requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD src /app/src