FROM python:3.8.2

RUN mkdir /api

COPY requirements.txt /api/requirements.txt

RUN pip install -r /api/requirements.txt

WORKDIR /api
