Answers
=======

Extraction
----------

``coala`` documentation is in ``rST`` files. ``docutils`` is used to parse rst
files.

``answers.extraction.Extractor`` is the ``NodeVisitor`` that visits all the
``section`` nodes. All the code text(``docutils.nodes.literal_block``) are
extracted and stored separately. All the normal text(all nodes excluding
``literal_block``) are extracted and stored separately. Filename, and section id
is appended at the end of the text for backtracking the file from the text.

.. note::
   If the node has a nested section node, then the current node
   is ignored because the nested section nodes will be visited later as well.

Forming Graph
-------------

A huge graph is created from all the text that was extracted using the
extraction module.

Creating nodes and Edges
~~~~~~~~~~~~~~~~~~~~~~~~

For natural language processing ``spacy`` is used.

Iterating over all the tokens:
If `head <https://en.wikipedia.org/wiki/Head_(linguistics)>`_ of the token is
the same as the token, then the token is ignored. If not, then
`lemmatized <https://en.wikipedia.org/wiki/Lemmatisation>`_ form of token and
head of token are created and an edge is formed between them.

The edges represent the relation between the tokens of the sentence.

Holding information
~~~~~~~~~~~~~~~~~~~

Each node contains information about the sections, codes and texts they appear
in, all of which are stored as attributes of the node.

``node.sections`` is a list of section ids.
``node.code`` is a list of code of sections particular token appears in.
``node.text`` is a list of text of sections in which the token appears.


Scoring answers
~~~~~~~~~~~~~~~

1. Documentation Graph and Question Graph is created using the algorithm
   described in earlier sections.
2. Steps 3 and 4 are repeated for all the pair of nodes in Question Graph.
3. All the shortest path between the pair of nodes is found in the
   Documentation Graph found(if both nodes exist in the Documentation Graph).
4. For all the nodes in the shortest path, the score of the sections of these
   nodes are incremented.
5. The section with highest score is returned.

Rationale:

a. For using shortest path:
   Shortest path between the nodes give the number of different ways(sentences)
   in which the nodes are related to each other.
b. The scoring system:
   All the nodes in the path relate the two given nodes. Hence, the section in
   which these nodes occur most should give the content most relevant to the
   question.
