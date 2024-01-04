FROM python:3.10.13
MAINTAINER longjunli longjunli1990@gmail.com

RUN apt update && apt upgrade -y

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN rm /usr/bin/mysql*
COPY uwsgi.ini /uwsgi.ini
RUN pip freeze > newreqs.txt
