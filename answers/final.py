from collections import OrderedDict, Counter
import logging

from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess
import networkx
import nltk
import spacy

from .extraction import parse_docs


nlp = spacy.load('en_core_web_md')


def grapheize(graph, doc, attrs={}):
    """
    Create a graph from given piece of text. Nodes are formed from lemmatized
    tokens. Edges are created between a lemmatized token and lemma of head of
    the sentence that token belongs to.
    """
    unallowed_tags = [
        'EX', 'HVS', 'MD', 'PDT',
        'IN', 'DT', 'TO', 'CD',
        'CC', '-LRB-', 'HYPH', ':'
    ]
    for token in doc:
        if (token.tag_ in unallowed_tags) or (token == token.head):
            continue
        nodes = [token.lemma_, token.head.lemma_]
        for node in nodes:
            if node not in graph:
                graph.add_node(node, token=token)
            node = graph.node.get(node)
            for key, value in attrs.items():
                node.setdefault(key, []).append(value)
        graph.add_edge(*nodes)


def get_answer(question, graph, final=False):
    """
    yields top 3 relevant documents.

    Scoring:
    1. Question graph is created using ``grapheize`` function.
    2. The nodes in all the edges of question graph are searched in the
       documentation graph.
    3. Walk throught the shortest path between the nodes in the documentation
       graph and increase the score of all the documents in the node by 1.
    4. Scale down all the scores w.r.t to the max score.

    NOTE: There will always be one answer with score 1.
    """
    q_graph = networkx.Graph()
    q_doc = nlp(question)
    q_type = []
    for token in q_doc:
        if token.tag_.startswith('W'):
            q_type.append(token)

    grapheize(q_graph, q_doc, attrs={'q_type': q_type})
    scores = Counter()
    found_common = False
    for start, end in q_graph.edges():
        found_common = True
        if start in graph and end in graph:
            for path in networkx.algorithms.all_shortest_paths(
                    graph, start, end):

                for node in path:
                    scores.update(graph.node.get(node)['text'])

    sorted_counter = OrderedDict(sorted(scores.items(), key=lambda x: x[1],
                                        reverse=True))

    items = list(sorted_counter.items())
    if items:
        min_score = items[-1][1]
        max_score = items[0][1]
        diff_max_min = max_score - min_score

    for item in items:
        key = item[0]
        score = item[1]
        sorted_counter[key] = ((score - min_score) / diff_max_min)

    for doc, i in Counter(sorted_counter).most_common(3):
        yield (doc, i)


def construct_graph(data):
    """
    Construct graph from documentation.
    """
    graph = networkx.Graph()
    for name, doc in data.items():
        meta = {
            'section_name': name,
            'code': doc['code'],
            'text': doc['text']
        }
        grapheize(graph, nlp(doc['text']), meta)
    return graph


if __name__ == '__main__':
    data = parse_docs()
    graph = construct_graph(data)
    try:
        def mod(y): return map(lambda x: (x[0][:100], x[1]), y)
        while True:
            q = input('>> ')
            print(list(mod(list(get_answer(q, graph)))))
    except KeyboardInterrupt:
        print('exiting...')
