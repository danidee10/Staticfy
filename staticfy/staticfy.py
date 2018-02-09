"""Staticfy.py."""

import re
import os
import sys
import json
import errno
import codecs
import argparse

from bs4 import BeautifulSoup

from .config import frameworks


def makedir(path):
    """Function to emulate exist_ok in python > 3.3 (mkdir -p in *nix)."""
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_asset_location(element, attr):
    """
    Get Asset Location.

    Remove leading slash e.g '/static/images.jpg' ==> static/images.jpg
    Also, if the url is also prefixed with static, it would be removed.
        e.g static/image.jpg ==> image.jpg
    """
    asset_location = re.match(r'^/?(static)?/?(.*)', element[attr],
                              re.IGNORECASE)

    # replace relative links i.e (../../static)
    asset_location = asset_location.group(2).replace('../', '')

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


def get_elements(html_file, tags):
    """
    Extract all the elements we're interested in.

    Returns a list of tuples with the attribute as first item
    and the list of elements as the second item.
    """
    with open(html_file) as f:
        document = BeautifulSoup(f, 'html.parser')

        def condition(tag, attr):
            # Don't include external links
            return lambda x: x.name == tag \
                and not x.get(attr, 'http').startswith(('http', '//'))

        all_tags = [(attr, document.find_all(condition(tag, attr)))
                    for tag, attr in tags]

        return all_tags


def replace_lines(html_file, transformed):
    """Replace lines in the old file with the transformed lines."""
    result = []
    with codecs.open(html_file, 'r', 'utf-8') as input_file:
        for line in input_file:
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


def staticfy(html_file, args=argparse.ArgumentParser()):
    """
    Staticfy method.

    Loop through each line of the file and replaces the old links
    """
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

    # get elements we're interested in
    matches = get_elements(html_file, tags)

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


def main():
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

    staticfied = staticfy(html_file, args=args)
    file_ops(staticfied, args=args)


if __name__ == '__main__':
    main()
