FROM python:3.9-alpine
WORKDIR /app

COPY requirements.txt ./
RUN apk --no-cache add curl  \
    && apk --no-cache add \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY manage.py ./
COPY snippets ./snippets
