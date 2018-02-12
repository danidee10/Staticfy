#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Staticfy',
      version='2.0',
      description='Convert static assets links to dynamic web framework links',
      url='https://github.com/danidee10/Staticfy',
      author='Osaetin Daniel',
      author_email='osaetindaniel@gmail.com',
      license='GPL',
      scripts=['bin/staticfy'],
      packages=find_packages(),
      install_requires=[
          'beautifulsoup4', 'pyyaml'
      ],
      zip_safe=False)
