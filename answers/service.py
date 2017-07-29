import json
import os

from flask import Flask, jsonify, request
from gensim.summarization import summarize

from .final import get_answer, construct_graph
from .extraction import parse_docs

app = Flask(__name__)

DATA = parse_docs()
GRAPH = construct_graph(DATA)


@app.route('/answer')
def serve_answer():
    global GRAPH
    return jsonify(list(get_answer(request.args.get('question'), GRAPH)))


@app.route('/summarize')
def serve_summary():
    try:
        summary = summarize(request.args.get('text'))
    except ValueError:
        summary = request.args.get('text')
    return jsonify({'res': summarize(request.args.get('text'))})
