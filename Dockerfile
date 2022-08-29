FROM python:3.9-alpine3.16
WORKDIR /app
COPY . .
RUN chmod +x wait-for-db.sh entrypoint.sh
RUN apk update \
    && apk add bash \
    && apk add python3 postgresql-libs \
    && apk add --update --no-cache --virtual .build-deps alpine-sdk python3-dev musl-dev postgresql-dev libffi-dev \
    && pip install -U setuptools pip \
    && pip install --no-cache-dir -r requirements.txt \