#!/usr/bin/env python

from setuptools import setup

setup(name='Staticfy',
      version='0.1',
      description='Convert static assets links to dynamic web framework links',
      url='https://github.com/danidee10/funniest',
      author='Osaetin Daniel',
      author_email='osaetindaniel@gmail.com',
      license='GPL',
      packages=['staticfy'],
      install_requires=[
          'beautifulsoup4',
      ],
      zip_safe=False)
