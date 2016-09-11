#! /usr/bin/python3
from bs4 import BeautifulSoup
import sys
import re
import os
import argparse

def parse_cmd_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, nargs='?', help='Filename of the file to be staticfied')
    parser.add_argument('--static-endpoint', help='static endpoint which is usually == "static"')
    parser.add_argument('--template-folder', help='template folder that contains the html file(s)')
    args = parser.parse_args()

    filename, static_endpoint, template_folder = args.filename, args.static_endpoint, args.template_folder

    if not filename and template_folder:
        # get all the files in the folder and staticfy them
        for file in os.scandir(template_folder):
            if file.name.endswith(('htm', 'html')) and file.is_file():
                staticfy(file.name, static_endpoint=static_endpoint, template_folder=template_folder)
    else:
        staticfy(filename, static_endpoint=static_endpoint, template_folder=template_folder)



def staticfy(filename, static_endpoint='static', template_folder=''):

    results = []  # list that holds the links, images and scripts as they're found by BeautifulSoup
    static_url = static_endpoint or 'static' # incase None is passed as the static_endpoint
    template_folder = template_folder or '' # incase None is passed as the template_folder

    in_file = os.path.join(template_folder, filename)

    try:
        file_handle = open(in_file)
    except FileNotFoundError as e:
        print('\033[91m' + 'File not found' + '\033[0m')
        sys.exit(1)

    html_doc = BeautifulSoup(file_handle, 'html.parser')

    # find all images in the file
    image_links = html_doc.find_all('img', src=True)

    # protect against external links like Google fonts, FontAwesome etc
    links = html_doc.find_all(lambda x: True if x.name == 'link' and not x.get('href').startswith(('http', '//')) else False)

    # find all script tags
    scripts = html_doc.find_all('script', src=True)

    # Do the actual replacement and store the results in a list
    for link in links:
        res = (link['href'], "{{{{ url_for('{}', filename='{}') }}}}".format(static_url, link['href']))
        results.append(res)

    for image in image_links:
        res = (image['src'], "{{{{ url_for('{}', filename='{}') }}}}".format(static_url, image['src']))
        results.append(res)

    for script in scripts:
        res = (script['src'], "{{{{ url_for('{}', filename='{}') }}}}".format(static_url, script['src']))
        results.append(res)

    file_handle.close()

    # create the staticfy and the appropriate template folder
    template_folder = template_folder.split(os.path.sep)[-1]
    filename = filename.split(os.path.sep)[-1] # incase filename is a link to a path

    out_file = os.path.join('staticfy', filename)
    os.makedirs(os.path.dirname(out_file), exist_ok=True)

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
                # print(file_line) --verbose option
                output_file.write(file_line)

        print('staticfied \033[94m{} ==> \033[92m{}\033[0m\n'.format(in_file, out_file))

        return out_file

if __name__ == '__main__':
    parse_cmd_arguments()
