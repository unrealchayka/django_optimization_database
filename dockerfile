# главное изображение
FROM python:3.9-alpine3.16

# копирование зависимостей
COPY requirements.txt /temp/requirements.txt
# копирование главной папки 
COPY service service/

# рабочая директория 
WORKDIR /service
# порт
EXPOSE 8001

# 
RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user