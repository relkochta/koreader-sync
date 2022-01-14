FROM python:3

MAINTAINER Ryan El Kochta "relkochta@lightn1ng.space"

RUN apt-get update -y && \
    apt-get install -y python3-flask gunicorn

WORKDIR /usr/src/app
COPY . .

ENV KOSYNC_SQLITE3_DB=/data/sqlite3.db

CMD [ "gunicorn", "--bind=0.0.0.0:8080", "kosync:app" ]

