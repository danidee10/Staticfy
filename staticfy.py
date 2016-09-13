#! /usr/bin/python3
from bs4 import BeautifulSoup
import sys
import re
import os
import errno
import argparse
import json

def makedir(path):
    # function to emulate exist_ok in Python >3.3 which works like mkdir -p in linux
    try:
        os.makedirs(path)
    except OSError as e:  # Python >2.5
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def staticfy(file, *args, **kwargs):

    results = []  # list that holds the links, images and scripts as they're found by BeautifulSoup
    tags = {'img': 'src', 'link': 'href', 'script': 'src'}
    add_tags = kwargs.get('add_tags') or {} # incase None is passed
    static_url = kwargs.get('static_endpoint') or 'static' # incase None is passed as the static_endpoint
    all_tags = [tags, add_tags]

    file_handle = open(file)

    html_doc = BeautifulSoup(file_handle, 'html.parser')

    for tags in all_tags:
        for tag, attr in tags.items():
            all_tags = html_doc.find_all(lambda x: True if x.name == tag and not x.get(attr, 'http').startswith(('http', '//')) else False)

            for elem in all_tags:
                """ store elem as a tuple with three elements to identify matching lines in the files during replacement
                (
                   'src',
                   'images/staticfy.jpg',
                   "{{ url_for('static', filename='images/staticfy.jpg') }}"
                )
                """
                res = (attr, elem[attr], "{{{{ url_for('{}', filename='{}') }}}}".format(static_url, elem[attr]))
                results.append(res)

    file_handle.close()

    filename = file.split(os.path.sep)[-1] # incase filename is a link to a path
    # create the staticfy and the appropriate template folder
    out_file = os.path.join('staticfy', filename)
    makedir(os.path.dirname(out_file))

    # open files and start replacing matching lines
    with open(file, 'r') as input_file, open(out_file, 'w+') as output_file:
        for file_line in input_file:
            for attr, value, new_link in results:
                if attr in file_line and value in file_line:
                    file_line = re.sub(r'\'', '"', file_line)  # replace all single quotes with double quotes
                    file_line = file_line.replace(value, new_link)   # replace old link with new staticfied link
                    # print(file_line) verbose
                    output_file.write(file_line)
                    break
            else:
                output_file.write(file_line)

        print('staticfied \033[94m{} ==> \033[92m{}\033[0m\n'.format(file, out_file))

        return out_file

def parse_cmd_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='Filename or directory to be staticfied')
    parser.add_argument('--static-endpoint', help='static endpoint which is "static" by default')
    parser.add_argument('--add-tags', type=str, help='additional tags to staticfy')
    args = parser.parse_args()

    return args

def main():
    args = parse_cmd_arguments()
    file = args.file
    static_endpoint  = args.static_endpoint
    add_tags = args.add_tags

    if add_tags:
        try:
            add_tags = json.loads(args.add_tags)
        except ValueError:
            print('\033[91m' + 'Invalid json string: please provide a valid json string e.g {}'.format('\'{"img": "data-url"}\'') + '\033[0m')
            sys.exit(1)

    try:
        if os.path.isfile(file) and file.endswith(('htm', 'html')):
            staticfy(file, static_endpoint=static_endpoint, add_tags=add_tags)
        else:
            # it's a directory so loop through and staticfy
            for filename in os.listdir(file):
                if filename.endswith(('htm', 'html')):
                    template_folder = directory = file + os.path.sep + filename
                    staticfy(template_folder, static_endpoint=static_endpoint, add_tags=add_tags)

    except IOError:
        print('\033[91m' + 'Unable to read/find the specified file or directory' + '\033[0m')

if __name__ == '__main__':
    main()
