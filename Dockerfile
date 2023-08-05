FROM python:3.9-alpine
WORKDIR /app

RUN apk --no-cache add curl
RUN apk --no-cache add zip

COPY snippets ./snippets
COPY manage.py ./
COPY requirements.txt ./
COPY setup.py ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt