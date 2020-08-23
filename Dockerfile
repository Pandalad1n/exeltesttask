FROM python:3.7-slim-buster

RUN apt-get update \
 && apt-get install gcc -y \
 && apt-get clean