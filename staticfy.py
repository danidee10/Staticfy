#! /usr/bin/python3
from bs4 import BeautifulSoup
import sys
import re
import os
import errno
import argparse

tags = {'img': 'src', 'link': 'href', 'script': 'src'}

# check if we're running python2 or python3, to set FileNotFoundError
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

class StaticfyError(Exception):
    """custom exception class to properly handle IOError(for testing) when it is raised"""
    def __init__(self, message):
        self.message = message

        super(StaticfyError, self).__init__(message)

def makedir(path):
    # function to emulate exist_ok in Python >3.3 which works like mkdir -p in linux
    try:
        os.makedirs(path)
    except OSError as e:  # Python >2.5
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def parse_cmd_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, nargs='?', default='', help='Filename of the file to be staticfied')
    parser.add_argument('--static-endpoint', help='static endpoint which is "static" by default')
    parser.add_argument('--template-folder', help='template folder that contains the html file(s)')
    args = parser.parse_args()

    filename, static_endpoint, template_folder = args.filename, args.static_endpoint, args.template_folder

    if not filename and template_folder:
        # get all the files in the folder and staticfy them
        try:
            for file in os.listdir(template_folder):
                if file.endswith(('htm', 'html')) and os.path.isfile(template_folder + '/' + file):
                    staticfy(file, static_endpoint=static_endpoint, template_folder=template_folder)
        except OSError:
            print('\033[91m' + 'Unable to read or find the specified directory' + '\033[0m')

    elif not filename and not template_folder:
        parser.print_help()
    else:
        try:
            staticfy(filename, static_endpoint=static_endpoint, template_folder=template_folder)
        except StaticfyError as e:
            # if the file wasn't found or couldn't be read hide the traceback and print the error message
            sys.tracebacklimit = 0
            print(e.message)



def staticfy(filename, static_endpoint='static', template_folder=''):

    results = []  # list that holds the links, images and scripts as they're found by BeautifulSoup
    static_url = static_endpoint or 'static' # incase None is passed as the static_endpoint
    template_folder = template_folder or '' # incase None is passed as the template_folder

    in_file = os.path.join(template_folder, filename)

    try:
        file_handle = open(in_file)
    except FileNotFoundError:
        raise StaticfyError('\033[91m' + 'Unable to read or find the specified file' + '\033[0m')

    html_doc = BeautifulSoup(file_handle, 'html.parser')

    for tag, value in tags.items():
        all_tags = html_doc.find_all(lambda x: True if x.name == tag and not x.get(value).startswith(('http', '//')) else False)

        for elem in all_tags:
            res = (elem[value], "{{{{ url_for('{}', filename='{}') }}}}".format(static_url, elem[value]))
            results.append(res)

    file_handle.close()

    # create the staticfy and the appropriate template folder
    template_folder = template_folder.split(os.path.sep)[-1]
    filename = filename.split(os.path.sep)[-1] # incase filename is a link to a path

    out_file = os.path.join('staticfy', filename)
    makedir(os.path.dirname(out_file))

    with open(in_file, 'r') as input_file, open(out_file, 'w+') as output_file:
        for file_line in input_file:
            for key, line in results:
                if key in file_line:
                    file_line = re.sub(r'\'', '"', file_line)  # replace all single quotes with double quotes
                    file_line = file_line.replace(key, line)   # substitute link for new flask static link
                    # print(file_line) verbose
                    output_file.write(file_line)
                    break
            else:
                output_file.write(file_line)

        print('staticfied \033[94m{} ==> \033[92m{}\033[0m\n'.format(in_file, out_file))

        return out_file

if __name__ == '__main__':
    parse_cmd_arguments()
