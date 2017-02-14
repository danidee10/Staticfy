"""Staticfy.py."""
from bs4 import BeautifulSoup
import sys
import re
import os
import errno
import argparse
import json
from .__config__ import frameworks


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

    Removes leading slash e.g '/static/images.jpg' ==> static/images.jpg
    Also, if the url is also prefixed with static, it would be removed.
        e.g static/image.jpg ==> image.jpg
    """
    asset_location = re.match(r'^/?(static)?/?(.*)', element[attr],
                              re.IGNORECASE)

    return asset_location.group(2)


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

            res = (attribute, element[attribute], frameworks[framework] %
                   {'static_endpoint': static_endpoint, 'namespace': namespace,
                    'asset_location': asset_location})
            transformed.append(res)

    return transformed


def get_elements(html_file, tags):
    """
    Extract all the elements we're interested in.

    Returns a list of dicts with the attribute as the key and matching tags as
    a list
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


def staticfy(html_file, add_tags={}, exc_tags={}, framework='flask',
             namespace='', static_endpoint='static'):
    """
    Staticfy method.

    Loop through each line of the file and replaces the old links
    """
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

    # Replace lines
    result = []
    with open(html_file, 'r') as input_file:
        for line in input_file:
            # replace all single quotes with double quotes
            new_line = re.sub(r'\'', '"', line)

            for attr, value, new_link in transformed:
                if attr in new_line and value in new_line:

                    # replace old link with new staticfied link
                    new_line = new_line.replace(value, new_link)

                    # print(new_line) --verbose
                    result.append(new_line)
                    break
            else:
                result.append(new_line)

        return ''.join(result)


def file_ops(staticfied, filename):
    """Recreate the file and place it in the 'staticfy' directory."""
    # create the staticfy and the appropriate template folder
    out_file = os.path.join('staticfy', filename)
    makedir(os.path.dirname(out_file))

    with open(out_file, 'w') as f:
        f.write(staticfied)

    print('staticfied \033[94m{} ==> \033[92m{}\033[0m\n'.
          format(filename, out_file))


def parse_cmd_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, nargs='+',
                        help='Filename or directory to be staticfied')
    parser.add_argument('--static-endpoint',
                        help='static endpoint which is "static" by default')
    parser.add_argument('--add-tags', type=str,
                        help='additional tags to staticfy')
    parser.add_argument('--exc-tags', type=str, help='tags to exclude')
    parser.add_argument('--framework', type=str,
                        help='Web Framework (default: flask)')
    parser.add_argument('--namespace', type=str,
                        help='string to prefix url with')
    args = parser.parse_args()

    return args


def main():
    """Main method."""
    args = parse_cmd_arguments()
    files = args.file
    static_endpoint = args.static_endpoint  # if None is supplied
    add_tags = args.add_tags or '{}'
    exc_tags = args.exc_tags or '{}'
    framework = args.framework or os.getenv('STATICFY_FRAMEWORK', 'flask')
    namespace = args.namespace or ''

    try:
        add_tags = json.loads(add_tags)
        exc_tags = json.loads(exc_tags)
    except ValueError:
        print('\033[91m' + 'Invalid json string: please provide a valid json '
              'string e.g {}'.format('\'{"img": "data-url"}\'') + '\033[0m')
        sys.exit(1)

    for f in files:
        try:
            # import pdb; pdb.set_trace()
            if os.path.isfile(f) and f.endswith(('htm', 'html')):
                staticfied = staticfy(f, static_endpoint=static_endpoint,
                                      add_tags=add_tags, exc_tags=exc_tags,
                                      framework=framework, namespace=namespace)
                file_ops(staticfied, f)
            else:
                # it's a directory so loop through and staticfy
                for html_file in os.listdir(f):
                    if html_file.endswith(('htm', 'html')):
                        temp_filename = os.path.join(f, html_file)
                        staticfied = staticfy(temp_filename, add_tags=add_tags,
                                              static_endpoint=static_endpoint,
                                              exc_tags=exc_tags,
                                              framework=framework,
                                              namespace=namespace)
                        file_ops(staticfied, temp_filename)

        except IOError:
            print('\033[91m' + 'Unable to read/find the specified file or '
                               'directory' + '\033[0m')


if __name__ == '__main__':
    main()
