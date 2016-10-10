#! /usr/bin/python3
from bs4 import BeautifulSoup
import sys
import re
import os
import errno
import argparse
import json
from .__config__ import frameworks


def makedir(path):
    # function to emulate exist_ok in Python >3.3 which works like mkdir -p in
    # linux
    try:
        os.makedirs(path)
    except OSError as e:  # Python >2.5
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def staticfy(file_, static_endpoint='static', project_type='flask', **kwargs):
    results = []  # list that holds the links, images and scripts as they're found by BeautifulSoup
    add_tags = kwargs.get('add_tags', {}) # dangerous to set keyword args as a dict.
    exc_tags = kwargs.get('exc_tags', {})
    tags = {'img': 'src', 'link': 'href', 'script': 'src'}

    # remove tags if any
    tags = {k: v for k, v in tags.items() if k not in exc_tags}
    all_tags = [tags, add_tags]

    file_handle = open(file_)

    html_doc = BeautifulSoup(file_handle, 'html.parser')

    def condition(tag):
        return lambda x: x.name == tag\
            and not x.get(attr, 'http').startswith(('http', '//'))

    for tags in all_tags:
        for tag, attr in tags.items():
            all_tags = html_doc.find_all(condition(tag))

            for elem in all_tags:
                """ store elem as a tuple with three elements to identify
                 matching lines in the files during replacement
                (
                   'src',
                   'images/staticfy.jpg',
                   "{{ url_for('static', filename='images/staticfy.jpg') }}"
                )

                ============================================================
                remove leading slash e.g '/static/images.jpg' if any
                also, if the url is also prefixed with static,
                e.g static/image.jpg remove the prefix 'static'
                ============================================================
                """
                rem_prefix = elem[attr][1:] if elem[attr].startswith('/') else elem[attr]
                attr_prefix = rem_prefix.split('/')
                asset_location = '/'.join(attr_prefix[1:]) if attr_prefix[0] == 'static' else '/'.join(attr_prefix)

                res = (attr, elem[attr], frameworks[project_type] %
                {'static_endpoint':static_endpoint, "asset_location":asset_location})
                results.append(res)

    file_handle.close()

    # extract the filename incase the filename is a path html_files/[home.html]
    filename = file_.split(os.path.sep)[-1]

    # create the staticfy and the appropriate template folder
    out_file = os.path.join('staticfy', filename)
    makedir(os.path.dirname(out_file))

    # open files and start replacing matching lines
    with open(file_, 'r') as input_file, open(out_file, 'w+') as output_file:
        for file_line in input_file:
            # replace all single quotes with double quotes
            file_line = re.sub(r'\'', '"', file_line)

            for attr, value, new_link in results:
                if attr in file_line and value in file_line:

                    # replace old link with new staticfied link
                    file_line = file_line.replace(value, new_link)

                    # print(file_line) --verbose
                    output_file.write(file_line)
                    break
            else:
                output_file.write(file_line)

        print('staticfied \033[94m{} ==> \033[92m{}\033[0m\n'.format(
            file_, out_file))

        return out_file


def parse_cmd_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, nargs='+',
                        help='Filename or directory to be staticfied')
    parser.add_argument('--static-endpoint',
                        help='static endpoint which is "static" by default')
    parser.add_argument('--add-tags', type=str,
                        help='additional tags to staticfy')
    parser.add_argument('--project-type', type=str,
                        help='Project Type (default: flask)')
    parser.add_argument('--exc-tags', type=str, help='tags to exclude')
    args = parser.parse_args()

    return args


def main():
    args = parse_cmd_arguments()
    files = args.file
    static_endpoint = args.static_endpoint or 'static' # if it's None
    project_type = args.project_type or os.getenv('STATICFY_FRAMEWORK', 'flask')
    add_tags = args.add_tags or '{}'
    exc_tags = args.exc_tags or '{}'

    try:
        add_tags = json.loads(add_tags)
        exc_tags = json.loads(exc_tags)
    except ValueError:
        print('\033[91m' + 'Invalid json string: please provide a valid json string e.g {}'.format(
            '\'{"img": "data-url"}\'') + '\033[0m')
        sys.exit(1)

    for file_ in files:
        try:
            if os.path.isfile(file_) and file_.endswith(('htm', 'html')):
                staticfy(file_, static_endpoint=static_endpoint, add_tags=add_tags,
                         exc_tags=exc_tags, project_type=project_type)
            else:
                # it's a directory so loop through and staticfy
                for filename in os.listdir(file_):
                    if filename.endswith(('htm', 'html')):
                        temp_filename = file_ + os.path.sep + filename
                        staticfy(temp_filename, static_endpoint=static_endpoint,
                                 add_tags=add_tags, exc_tags=exc_tags, project_type=project_type)

        except IOError:
            print(
                '\033[91m' + 'Unable to read/find the specified file or directory' + '\033[0m')
