FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir spa

WORKDIR spa

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY payment .


RUN chmod a+x docker/*.sh