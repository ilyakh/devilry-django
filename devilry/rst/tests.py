"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from docutils.parsers.rst import directives
from docutils.nodes import Element
from docutils.parsers.rst import Directive


class testdirective(Element): pass

class TestDirective(Directive):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    # The options to the directive
    option_spec = {
            'font-size': directives.positive_int}

    # Does it have content (in addition to arguments and options)?
    has_content = False

    def run(self):
        arg = directives.unchanged_required(self.arguments[0])
        if arg != "test":
            raise self.error('Argument must be "test"!')
        self.options['arg'] = arg
        node = testdirective(rawsource='', **self.options)
        return [node]
    


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

