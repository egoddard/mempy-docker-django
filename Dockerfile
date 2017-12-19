FROM python:3
ENV PYTHONBUFFERED 1

# App setup
RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/
