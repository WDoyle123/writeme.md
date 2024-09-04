FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt /app

RUN apk add --no-cache \
    && apk add --no-cache --virtual .build-deps \
        build-base \
        pkgconf \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apk del .build-deps

COPY . /app

CMD ["python3", "consumer.py"]

