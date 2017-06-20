FROM python:3-alpine

ENV COBOT_ROOT=/opt/errbot

ADD requirements.txt $COBOT_ROOT/requirements.txt

RUN apk add --no-cache libffi openssl git \
    && apk add --no-cache --virtual .build-deps \
           gcc \
           libc-dev \
           libffi-dev \
           openssl-dev \
    && pip install -r $COBOT_ROOT/requirements.txt \
    && apk del .build-deps

ADD . $COBOT_ROOT

RUN addgroup -S errbot \
    && adduser -h $COBOT_ROOT -G errbot -S errbot \
    && mkdir -p $COBOT_ROOT/data $COBOT_ROOT/plugins \
    && chown -R errbot:errbot $COBOT_ROOT

USER errbot
WORKDIR /opt/errbot
CMD errbot
