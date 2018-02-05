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


def transform(file):
    """Transform posthtml to django templates."""
    result = []

    for line in file:
        
        line = transform_extends_tag(line)

        result.append(line)

    return result
