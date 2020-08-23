FROM python:3.7-slim-buster
WORKDIR /app
RUN apt-get update \
 && apt-get install gcc -y \
 && apt-get clean

ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . .

ENV FLASK_APP /app/web.py

EXPOSE 80
CMD flask run --host 0.0.0.0 --port 80
