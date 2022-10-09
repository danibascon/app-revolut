#######################    BASE    #######################
FROM python:3.7.3-alpine3.9 as base

WORKDIR /app

COPY main.py .
COPY requirements.txt .
COPY getenv.py .

RUN pip install -r requirements.txt

ENV FLASK_APP=main.py
ENV FLASK_ENV=dev
ENV MONGO_INITDB_ROOT_USERNAME=
ENV MONGO_INITDB_ROOT_PASSWORD=
ENV MONGO_INITDB_DATABASE=
ENV MONGO_INITDB_HOST_NAME=
#######################    PROD    #######################
FROM base as prod

EXPOSE 5000

CMD flask run -h 0.0.0.0 -p 5000