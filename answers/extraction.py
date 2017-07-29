"""
Handles the parsing and extraction of information from rST doc files.
"""

import os

import docutils
import docutils.nodes
import docutils.parsers.rst

from .utils import get_abs_path


class IgnoredDirective(docutils.parsers.rst.Directive):

    """Stub for unknown directives."""

    has_content = True

    def run(self):
        """Do nothing."""
        return []


docutils.parsers.rst.directives.register_directive('seealso', IgnoredDirective)
docutils.parsers.rst.directives.register_directive('argparse', IgnoredDirective)


class Extractor(docutils.nodes.SparseNodeVisitor):
    """
    Node visitor to extract information from nodes.
    """

    def __init__(self, document, data, name=''):
        super().__init__(document)
        self.name = name
        self.data = data

    def visit_section(self, node):
        non_section_childs = list(filter(
            lambda x: type(x) != docutils.nodes.section, node.children
        ))
        handle_non_section_nodes(node, non_section_childs, self.name, self.data)


def parse_rst(path):
    """
    :param path: The path of the rst file.
    :return: The document object
    """
    rst = open(path)
    default_settings = docutils.frontend.OptionParser(
        components=(docutils.parsers.rst.Parser, )
        ).get_default_values()
    document = docutils.utils.new_document(rst.name, default_settings)
    parser = docutils.parsers.rst.Parser()
    parser.parse(rst.read(), document)
    rst.close()
    return document


def handle_non_section_nodes(section_node, non_section_child_nodes, doc_name,
                             data):
    """
    All the nodes that are not section nodes are parsed here.
    """
    non_code_nodes = filter(
        lambda x: type(x) not in [docutils.nodes.literal_block],
        non_section_child_nodes
    )
    code_nodes = filter(lambda x: type(x) in [docutils.nodes.literal_block],
                        non_section_child_nodes)
    code = '\n'.join(map(lambda x: x.astext(), code_nodes))
    text = '\n'.join(map(lambda x: x.astext(), non_code_nodes))

    data[section_node.get('ids')[0]] = {
        "code": code,
        "text": (text + '\n' + doc_name[:-4] + '.html#' +
                 section_node.get('ids')[0]),
        "file": doc_name
    }


def parse_docs():
    """
    Parse all documentation files and store information in data.
    """
    data = {}
    for files in os.listdir(get_abs_path('coala/docs/Developers')):
        rst = parse_rst(get_abs_path('coala/docs/Developers/' + files))
        extractor = Extractor(rst, data, files)
        rst.walk(extractor)
    return data
