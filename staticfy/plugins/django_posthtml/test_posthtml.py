"""Tests for the django plugin."""

import unittest

from .posthtml import transform


class DjangoTestCase(unittest.TestCase):
    """Tests for the django plugin."""

    def test_extends_tag(self):
        """
        The <extends> tag should be converted to {% extends ".*" %}.
        
        The closing </extends> tag should also be removed.
        """
        result = transform(
            ['<extends src="base.html">', '<p>Hello world</p>', '</extends>']
        )

        expected = ['{% extends "base.html" %}', '<p>Hello world</p>', '']

        self.assertEqual(result, expected)

    def test_include_tag(self):
        """The <include> tag should be converted to {% include ".*" %}."""
        result = transform(
            ['<include src="base.html"></include>', '<p>Hello world</p>']
        )

        expected = ['{% include "base.html" %}', '<p>Hello world</p>']

        self.assertEqual(result, expected)

    def test_block_tag(self):
        """
        The <block> tag should be converted to {% block .* %}.
        
        The closing </block> tag should be converted to {% endblock %}
        """
        result = transform(
            ['<block name="content">', '<p>Hello world</p>', '</block>']
        )

        expected = ['{% block content %}', '<p>Hello world</p>', '{% endblock %}']

        self.assertEqual(result, expected)

    def test_include_static_tag(self):
        pass


if __name__ == '__main__':
    unittest.main()