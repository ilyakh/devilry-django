"""
Wrapper for reStructuredText.
"""

from docutils.parsers.rst import Parser
from docutils.utils import Reporter, decode_path
from docutils import nodes
from docutils import frontend
from docutils.parsers.rst import directives
from docutils.nodes import Element
from docutils.parsers.rst import Directive



class RstValidationError(Exception):
    def __init__(self, level, line, message):
        self.level = level
        self.line = line
        self.message = message

    def __str__(self):
        return 'line %s: %s' % (self.line, self.message)

class ExceptionReporter(Reporter):
    """ Report errors as exceptions. """
    def __init__(self, source):
        Reporter.__init__(self, source,
                report_level = 0,
                halt_level = 0,
                stream = '',  # suppress output to terminal (only use exceptions)
                debug = 0,
                encoding = 'utf-8')

    def system_message(self, level, message, *children, **kwargs):
        raise RstValidationError(level, kwargs.get('line'), message)


def rstdoc_from_string(rst):
    parser = Parser()
    settings = frontend.OptionParser().get_default_values()
    settings.tab_width = 4
    settings.pep_references = False
    settings.rfc_references = False
    settings.embed_stylesheet = False

    source_path = decode_path('string')
    reporter = ExceptionReporter(source_path)
    document = nodes.document(settings, reporter, source=source_path)
    document.note_source(source_path, -1)

    parser.parse(rst, document)
    return document

