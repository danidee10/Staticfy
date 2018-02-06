#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Staticfy',
      version='1.7',
      description='Convert static assets links to dynamic web framework links',
      url='https://github.com/danidee10/Staticfy',
      author='Osaetin Daniel',
      author_email='osaetindaniel@gmail.com',
      license='GPL',
      scripts = ['bin/staticfy'],
      packages=find_packages(),
      install_requires=[
          'beautifulsoup4',
      ],
      zip_safe=False)
