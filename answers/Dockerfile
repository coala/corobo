FROM python:3

ENV ROOT=/app

ADD requirements.txt $ROOT/requirements.txt

RUN apt-get -y update && apt-get install -y gcc gfortran git \
    && git clone https://github.com/coala/coala /app/coala \
    && git clone https://github.com/coala/documentation /app/documentation \
    && pip install -U pip -r $ROOT/requirements.txt \
    && apt-get remove -y gcc gfortran git \
    && python -m spacy download en_core_web_md

ADD . $ROOT

WORKDIR /app
EXPOSE 8000
CMD gunicorn -t 120 service:app -b 0.0.0.0:8000
