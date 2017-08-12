import json
import os

from flask import Flask, jsonify, request
from gensim.summarization import summarize

from final import get_answer, construct_graph
from extraction import parse_docs

app = Flask(__name__)

DATA = parse_docs()
GRAPH = construct_graph(DATA)


@app.route('/answer')
def serve_answer():
    global GRAPH
    return jsonify(list(get_answer(request.args.get('question'), GRAPH)))


@app.route('/summarize', methods=['POST'])
def serve_summary():
    try:
        summary = summarize(request.get_json().get('text'))
    except ValueError:
        summary = request.get_json().get('text')
    return jsonify({'res': summary})
