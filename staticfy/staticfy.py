"""Staticfy.py."""

import os
import re
import sys
import json
import argparse
from importlib import import_module

from bs4 import BeautifulSoup

from .config import frameworks


def get_asset_location(element, attr):
    """
    Get Asset Location.

    Remove leading slash e.g '/static/images.jpg' ==> static/images.jpg
    Also, if the url is also prefixed with static, it would be removed.
        e.g static/image.jpg ==> image.jpg
    """
    asset_location = re.match(r'^/?(static)?/?(.*)', element[attr],
                              re.IGNORECASE)

    # replace relative links i.e (../../static) or (./)
    asset_location = asset_location.group(2).replace('../', '')
    asset_location = asset_location.replace('./', '')

    return asset_location


def transform(matches, framework, namespace, static_endpoint):
    """
    The actual transformation occurs here.

    flask example: images/staticfy.jpg', ==>
        "{{ url_for('static', filename='images/staticfy.jpg') }}"
    """
    transformed = []
    namespace = namespace + '/' if namespace else ''

    for attribute, elements in matches:
        for element in elements:
            asset_location = get_asset_location(element, attribute)

            # string substitution
            sub_dict = {
                'static_endpoint': static_endpoint, 'namespace': namespace,
                'asset_location': asset_location
            }
            transformed_string = frameworks[framework] % sub_dict

            res = (attribute, element[attribute], transformed_string)
            transformed.append(res)

    return transformed


def transform_using_plugins(html_file, plugins):
    """
    Transform the html file using specified plugins.

    Save at the end of the transformation
    """

    with open(html_file) as file:
        transformed = [line for line in file]

        for plugin_name in plugins:
            plugin = import_module('plugins.' + plugin_name)
            transformed = plugin.transform(transformed)

    if plugins:
        return transformed


def get_elements(html, html_file, tags):
    """
    Extract all the elements we're interested in.

    Returns a list of tuples with the attribute as first item
    and the list of elements as the second item.
    """

    document = BeautifulSoup(''.join(html), 'html.parser')

    def no_external_links(tag, attr):
        """Don't include external links."""
        return lambda x: x.name == tag \
            and not x.get(attr, 'http').startswith(('http', '//'))

    all_tags = [(attr, document.find_all(no_external_links(tag, attr)))
                for tag, attr in tags
                ]

    # Save contents back to file
    with open(html_file, 'w') as file:
        file.write(''.join(html))

    return all_tags


def replace_lines(html_file, transformed):
    """Replace lines in the old file with the transformed lines."""
    result = []

    with open(html_file) as file:
        for line in file:
            # replace all single quotes with double quotes
            line = re.sub(r'\'', '"', line)

            for attr, value, new_link in transformed:
                if attr in line and value in line:

                    # replace old link with new staticfied link
                    new_line = line.replace(value, new_link)

                    result.append(new_line)
                    break
            else:
                result.append(line)

    return ''.join(result)


def staticfy(html_file, config=None, args=argparse.ArgumentParser()):
    """
    Staticfy method.

    Loop through each line of the file and replaces the old links
    """

    if not config:
        config = {'plugins': ['django_posthtml']}

    # unpack arguments
    static_endpoint = args.static_endpoint or 'static'
    framework = args.framework or os.getenv('STATICFY_FRAMEWORK', 'flask')
    add_tags = args.add_tags or {}
    exc_tags = args.exc_tags or {}
    namespace = args.namespace or {}

    # default tags
    tags = {('img', 'src'), ('link', 'href'), ('script', 'src')}

    # generate additional_tags
    add_tags = {(tag, attr) for tag, attr in add_tags.items()}
    tags.update(add_tags)

    # remove tags if any was specified
    exc_tags = {(tag, attr) for tag, attr in exc_tags.items()}
    tags = tags - exc_tags

    # apply plugin(s) transformation
    html = transform_using_plugins(html_file, config['plugins'])

    # get elements we're interested in
    matches = get_elements(html, html_file, tags)

    # transform old links to new links
    transformed = transform(matches, framework, namespace, static_endpoint)

    return replace_lines(html_file, transformed)


def file_ops(staticfied, args):
    """Write to stdout or a file"""
    destination = args.o or args.output

    if destination:
        with open(destination, 'w') as file:
            file.write(staticfied)
    else:
        print(staticfied)


def parse_cmd_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str,
                        help='Filename to be staticfied')
    parser.add_argument('--static-endpoint',
                        help='Static endpoint which is "static" by default')
    parser.add_argument('--add-tags', type=str,
                        help='Additional tags to staticfy')
    parser.add_argument('--exc-tags', type=str, help='tags to exclude')
    parser.add_argument('--framework', type=str,
                        help='Web Framework: Defaults to Flask')
    parser.add_argument('--namespace', type=str,
                        help='String to prefix url with')
    parser.add_argument('-o', type=str, help='Specify output file')
    parser.add_argument('--output', type=str, help='Specify output file')
    args = parser.parse_args()

    return args


def main(config):
    """Main method."""
    args = parse_cmd_arguments()
    html_file = args.file

    try:
        json.loads(args.add_tags or '{}')
        json.loads(args.exc_tags or '{}')
    except ValueError:
        print('\033[91m' + 'Invalid json string: please provide a valid json '
              'string e.g {}'.format('\'{"img": "data-url"}\'') + '\033[0m')
        sys.exit(1)

    staticfied = staticfy(html_file, config=config, args=args)
    file_ops(staticfied, args=args)
