FROM python:3.6-alpine

ENV BOT_ROOT=/opt/errbot

ADD requirements.txt $BOT_ROOT/requirements.txt

RUN apk add --no-cache libffi openssl git \
    && apk add --no-cache --virtual .build-deps \
           gcc \
           libc-dev \
           libffi-dev \
           openssl-dev \
    && pip install -r $BOT_ROOT/requirements.txt \
    && pip install slackclient python-telegram-bot \
    && apk del .build-deps

ADD . $BOT_ROOT

RUN addgroup -S errbot \
    && adduser -h $BOT_ROOT -G errbot -S errbot \
    && mkdir -p $BOT_ROOT/data $BOT_ROOT/plugins \
    && chown -R errbot:errbot $BOT_ROOT

USER errbot
WORKDIR /opt/errbot
CMD errbot
