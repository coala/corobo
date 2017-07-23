FROM python:3

ENV ROOT=/app

ADD requirements.txt $ROOT/requirements.txt

RUN apt-get -y update && apt-get install -y gcc gfortran \
    && pip install -U pip -r $ROOT/requirements.txt \
    && apt-get remove -y gcc gfortran \
    && python -m spacy download en_core_web_md

ADD . $ROOT/answers

WORKDIR /app
CMD gunicorn -t 120 answers.service:app
