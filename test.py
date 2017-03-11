#! /usr/bin/python3
"""Run tests."""

import unittest
import os
from staticfy.staticfy import staticfy


class StaticfyTest(unittest.TestCase):
    """Test Case."""

    @classmethod
    def setUpClass(cls):
        """Setup file to be used for tests."""
        cls.filename = 'test.html'
        data = ("""<link rel='stylesheet' href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                """<img src="/static/images/staticfy.jpg" />\n"""
                """<img data-url="images/staticfy.jpg" />\n"""
                """<link rel="stylesheet" href='../css/style.css' />\n"""
                """<script src="/js/script.js">alert('hello world')</script>\n"""
                )

        with open(cls.filename, 'w+') as f:
            f.write(data)

    def test_normal_staticfy(self):
        """Testing Flask => {{ url_for('static', filename='css/style.css') }}."""
        result = staticfy(self.filename)

        expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                           """<img src="{{ url_for('static', filename='images/staticfy.jpg') }}" />\n"""
                           """<img data-url="images/staticfy.jpg" />\n"""
                           """<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" />\n"""
                           """<script src="{{ url_for('static', filename='js/script.js') }}">alert("hello world")</script>\n"""
                           )

        self.assertEqual(result, expected_result)

    def test_static_endpoint(self):
        """Testing Static endpoint."""
        result = staticfy(self.filename, static_endpoint='my_static')

        expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                           """<img src="{{ url_for('my_static', filename='images/staticfy.jpg') }}" />\n"""
                           """<img data-url="images/staticfy.jpg" />\n"""
                           """<link rel="stylesheet" href="{{ url_for('my_static', filename='css/style.css') }}" />\n"""
                           """<script src="{{ url_for('my_static', filename='js/script.js') }}">alert("hello world")</script>\n"""
                           )
        self.assertEqual(result, expected_result)

    def test_additional_tags(self):
        """Testing additional tags."""
        result = staticfy(self.filename, add_tags={'img': 'data-url'})

        expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                           """<img src="{{ url_for('static', filename='images/staticfy.jpg') }}" />\n"""
                           """<img data-url="{{ url_for('static', filename='images/staticfy.jpg') }}" />\n"""
                           """<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" />\n"""
                           """<script src="{{ url_for('static', filename='js/script.js') }}">alert("hello world")</script>\n"""
                           )
        self.assertEqual(result, expected_result)

    def test_exclusive_tags(self):
        """Testing exclusive tags."""
        res = staticfy(self.filename, exc_tags={'link': 'href', 'img': 'src'})

        expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                           """<img src="/static/images/staticfy.jpg" />\n"""
                           """<img data-url="images/staticfy.jpg" />\n"""
                           """<link rel="stylesheet" href="../css/style.css" />\n"""
                           """<script src="{{ url_for('static', filename='js/script.js') }}">alert("hello world")</script>\n"""
                           )
        self.assertEqual(res, expected_result)

    def test_cleanup_html(self):
        """Testing HTML cleanup."""
        result = staticfy(self.filename)

        expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                           """<img src="{{ url_for('static', filename='images/staticfy.jpg') }}" />\n"""
                           """<img data-url="images/staticfy.jpg" />\n"""
                           """<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" />\n"""
                           """<script src="{{ url_for('static', filename='js/script.js') }}">alert("hello world")</script>\n"""
                           )

        self.assertEqual(result, expected_result)

    def test_django_project(self):
        """Testing Django => {% static 'css/style.css' %}."""
        result = staticfy(self.filename, framework='django')

        expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                           """<img src="{% static 'images/staticfy.jpg' %}" />\n"""
                           """<img data-url="images/staticfy.jpg" />\n"""
                           """<link rel="stylesheet" href="{% static 'css/style.css' %}" />\n"""
                           """<script src="{% static 'js/script.js' %}">alert("hello world")</script>\n"""
                           )
        self.assertEqual(result, expected_result)

    def test_laravel_project(self):
        """Testing Laravel => {{ URL::asset('css/bootstrap.min.css') }}."""
        result = staticfy(self.filename, framework='laravel')

        expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                           """<img src="{{ URL::asset('images/staticfy.jpg') }}" />\n"""
                           """<img data-url="images/staticfy.jpg" />\n"""
                           """<link rel="stylesheet" href="{{ URL::asset('css/style.css') }}" />\n"""
                           """<script src="{{ URL::asset('js/script.js') }}">alert("hello world")</script>\n"""
                           )
        self.assertEqual(result, expected_result)

    def test_namespace(self):
        """Testing namespace."""
        result = staticfy(self.filename, framework='django', namespace='admin')

        expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                           """<img src="{% static 'admin/images/staticfy.jpg' %}" />\n"""
                           """<img data-url="images/staticfy.jpg" />\n"""
                           """<link rel="stylesheet" href="{% static 'admin/css/style.css' %}" />\n"""
                           """<script src="{% static 'admin/js/script.js' %}">alert("hello world")</script>\n"""
                           )
        self.assertEqual(result, expected_result)

    def test_replace_relative_links(self):
        """Testing replace_relative_links."""
        result = staticfy(self.filename, framework='django')

        expected_result = ("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.css" />\n"""
                           """<img src="{% static 'images/staticfy.jpg' %}" />\n"""
                           """<img data-url="images/staticfy.jpg" />\n"""
                           """<link rel="stylesheet" href="{% static 'css/style.css' %}" />\n"""
                           """<script src="{% static 'js/script.js' %}">alert("hello world")</script>\n"""
                           )
        self.assertEqual(result, expected_result)

    def test_filenotfound_exception(self):
        self.assertRaises(IOError, staticfy, 'Invalid file')

    @classmethod
    def tearDownClass(cls):
        """Remove test.html file."""
        os.remove(cls.filename)


if __name__ == '__main__':
    unittest.main()
