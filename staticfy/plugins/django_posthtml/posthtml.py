"""Django plugin for django templates."""

import re


def transform_extends_tag(html):
    """
    Convert <extends src=".*" /> to {% extends ".*" %}.

    Also remove the closing </extends> tag
    """
    opening_regex = r'<extends src=[\'"](.*)[\'"]>'
    closing_regex = r'</extends>'

    html = re.sub(opening_regex, r'{% extends "\1" %}', html)
    html = re.sub(closing_regex, '', html)

    return html


def transform_include_tag(html):
    """Convert <include src=".*"></include> to {% include ".*" %}."""
    include_regex = r'<include src=[\'"](.*/\w+/)*(\w+.html)[\'"]></include>'

    html = re.sub(include_regex, r'{% include "\2" %}', html)

    return html


def transform_block_tag(html):
    """
    Convert <block src=".*" /> to {% extends ".*" %}.

    Also convert the closing </block> to {% endblock %}
    """
    opening_regex = r'<block name=[\'"](.*)[\'"]>'
    closing_regex = r'</block>'

    html = re.sub(opening_regex, r'{% block \1 %}', html)
    html = re.sub(closing_regex, '{% endblock %}', html)

    return html


def transform(file):
    """Transform posthtml to django templates."""
    result = []

    for line in file:
        # Apply transforms
        line = transform_extends_tag(line)
        line = transform_include_tag(line)
        line = transform_block_tag(line)

        result.append(line)

    return result
