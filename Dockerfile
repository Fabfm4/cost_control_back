FROM python:3.10.4-slim-buster
ARG DB_URL_CONNECTION
ARG DB_DATABASE
ARG DB_ENGINE

ENV DB_URL_CONNECTION=$DB_URL_CONNECTION
ENV DB_DATABASE=$DB_DATABASE
ENV DB_ENGINE=$DB_ENGINE
ENV PORT=8000


WORKDIR /usr/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN echo ${DB_DATABASE}
RUN echo ${DB_URL_CONNECTION}

COPY ./src .
RUN touch .env
RUN echo "DB_URL_CONNECTION=${DB_URL_CONNECTION}" >> .env
RUN echo "DB_DATABASE=${DB_DATABASE}" >> .env
RUN echo "DB_ENGINE=${DB_ENGINE}" >> .env


CMD uvicorn main:app --host=0.0.0.0 --port=$PORT