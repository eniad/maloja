FROM python:3-alpine as base

WORKDIR /usr/src/app

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    libxml2-dev \
    libxslt-dev \
    py3-pip \
    libc-dev \
    linux-headers

RUN pip3 install psutil

# development
FROM base as dev

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN mkdir /data
COPY ./maloja/data_files /data

RUN apk add bash
RUN apk del .build-deps

EXPOSE 42010

# ENTRYPOINT /bin/bash
ENTRYPOINT python -m maloja.server

# production
FROM base

RUN pip3 install --upgrade --no-cache-dir malojaserver

RUN apk del .build-deps

EXPOSE 42010

ENTRYPOINT maloja run
