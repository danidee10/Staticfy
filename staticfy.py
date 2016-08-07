#! /usr/bin/python3

from bs4 import BeautifulSoup
import re
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--filename', help='Filename of the file to be staticfied', required=True)
parser.add_argument('--static-endpoint', help='static endpoint which is usually == "static"')
parser.add_argument('--template-folder', help='template folder that contains the html file(s)')
args = parser.parse_args()

results = []  # list that holds the links, images and scripts as they're found by BeautifulSoup
static_url = args.static_endpoint or 'static'  # fall back to the default static if no endpoint is specified
template_folder = args.template_folder or ''  # set template folder to an empty string if it wasn't provided

filename = args.filename
in_file = os.path.join(template_folder, filename)

file_handle = open(in_file)
html_doc = BeautifulSoup(file_handle, 'html.parser')

# find all images in the file
image_links = html_doc.find_all('img', src=True)

# protect against external links like Google fonts, FontAwesome etc
links = html_doc.find_all(lambda x: True if x.name == 'link' and not x.get('href').startswith(('http', '//')) else False)

# find all script tags
scripts = html_doc.find_all('script', src=True)

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
out_file = os.path.join('staticfy', template_folder, filename)
os.makedirs(os.path.dirname(out_file), exist_ok=True)

with open(in_file, 'r') as input_file, open(out_file, 'w') as output_file:
    for file_line in input_file:
        for key, line in results:
            if key in file_line:
                file_line = re.sub(r'\'', '"', file_line)  # replace all single quotes with double quotes
                file_line = file_line.replace(key, line)   # substitute link for new flask static link
                # print(file_line) verbose
                output_file.write(file_line)
                break
        else:
            # print(file_line)
            output_file.write(file_line)

    print('staticfied \033[94m{} ==> \033[92m{}\n'.format(in_file, out_file))

    # reset the terminal color back to it's normal color
    # os.system('cls||reset')  # dunno about windows ¯\_(ツ)_/¯
