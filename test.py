#! /usr/bin/python3

import unittest
import os
import shutil
from staticfy import staticfy

class StaticfyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = 'test.html'
        data = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                """<img src="/static/images/staticfy.jpg" />\n"""
                """<img data-url="images/staticfy.jpg" />\n"""
                """<link rel="stylesheet" href="css/style.css" />\n"""
                """<script src="/js/script.js">alert('hello world')</script>\n"""
                )

        with open(cls.filename, 'w+') as f:
            f.write(data)

    def test_normal_staticfy(self):
        out_file = staticfy(self.filename)

        with open(out_file, 'r') as f:
            file_contents = f.read()

            expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                               """<img src="{{ url_for('static', filename='images/staticfy.jpg') }}" />\n"""
                               """<img data-url="images/staticfy.jpg" />\n"""
                               """<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" />\n"""
                               """<script src="{{ url_for('static', filename='js/script.js') }}">alert("hello world")</script>\n"""
                               )

            self.assertEqual(file_contents, expected_result)

    def test_static_endpoint(self):
        out_file = staticfy(self.filename, static_endpoint='my_static')

        with open(out_file, 'r') as f:
            file_contents = f.read()

            expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                               """<img src="{{ url_for('my_static', filename='images/staticfy.jpg') }}" />\n"""
                               """<img data-url="images/staticfy.jpg" />\n"""
                               """<link rel="stylesheet" href="{{ url_for('my_static', filename='css/style.css') }}" />\n"""
                               """<script src="{{ url_for('my_static', filename='js/script.js') }}">alert("hello world")</script>\n"""
                               )
            self.assertEqual(file_contents, expected_result)

    def test_additional_tags(self):
        out_file = staticfy(self.filename, add_tags={'img': 'data-url'})

        with open(out_file, 'r') as f:
            file_contents = f.read()

            expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                               """<img src="{{ url_for('static', filename='images/staticfy.jpg') }}" />\n"""
                               """<img data-url="{{ url_for('static', filename='images/staticfy.jpg') }}" />\n"""
                               """<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" />\n"""
                               """<script src="{{ url_for('static', filename='js/script.js') }}">alert("hello world")</script>\n"""
                               )
            self.assertEqual(file_contents, expected_result)

    def test_exclusive_tags(self):
        out_file = staticfy(self.filename, exc_tags={'link': 'rel', 'img': 'src'})

        with open(out_file, 'r') as f:
            file_contents = f.read()

            expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                               """<img src="/static/images/staticfy.jpg" />\n"""
                               """<img data-url="images/staticfy.jpg" />\n"""
                               """<link rel="stylesheet" href="css/style.css" />\n"""
                               """<script src="{{ url_for('static', filename='js/script.js') }}">alert("hello world")</script>\n"""
                               )
            self.assertEqual(file_contents, expected_result)

    def test_django_project(self):
        out_file = staticfy(self.filename, project_type='django')

        with open(out_file, 'r') as f:
            file_contents = f.read()

            expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                               """<img src="{% static 'images/staticfy.jpg' %}" />\n"""
                               """<img data-url="images/staticfy.jpg" />\n"""
                               """<link rel="stylesheet" href="{% static 'css/style.css' %}" />\n"""
                               """<script src="{% static 'js/script.js' %}">alert("hello world")</script>\n"""
                               )
            self.assertEqual(file_contents, expected_result)

    def test_laravel_project(self):
        # laravel url's look like this {{ URL::asset('css/bootstrap.min.css') }}

        out_file = staticfy(self.filename, project_type='laravel')

        with open(out_file, 'r') as f:
            file_contents = f.read()
            expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                               """<img src="{{ URL::asset('images/staticfy.jpg') }}" />\n"""
                               """<img data-url="images/staticfy.jpg" />\n"""
                               """<link rel="stylesheet" href="{{ URL::asset('css/style.css') }}" />\n"""
                               """<script src="{{ URL::asset('js/script.js') }}">alert("hello world")</script>\n"""
                               )
            self.assertEqual(file_contents, expected_result)

    def test_filenotfound_exception(self):
        self.assertRaises(IOError, staticfy, 'Invalid file')

    @classmethod
    def tearDownClass(cls):
        # remove test.html and the staticy folder with all it's contents
        os.remove(cls.filename)
        shutil.rmtree('staticfy')


if __name__ == '__main__':
    unittest.main()
