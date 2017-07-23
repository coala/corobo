import json

from flask import Flask, jsonify, request
from gensim.summarization import summarize

from .final import graph, get_answer

app = Flask(__name__)


@app.route('/answer')
def serve_answer():
    global graph
    return jsonify(list(get_answer(request.args.get('question'), graph)))


@app.route('/summarize')
def serve_summary():
    try:
        summary = summarize(request.args.get('text'))
    except ValueError:
        summary = request.args.get('text')
    return jsonify({'res': summarize(request.args.get('text'))})
