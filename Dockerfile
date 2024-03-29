FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get -y install vim

WORKDIR /teenlief-backend

# 프로젝트 코드 복사
ADD . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt