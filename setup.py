#!/usr/bin/env python

from setuptools import setup

setup(name='Staticfy',
      version='0.1',
      description='Convert static assets links to dynamic web framework links',
      url='https://github.com/danidee10/Staticfy',
      author='Osaetin Daniel',
      author_email='osaetindaniel@gmail.com',
      license='GPL',
      py_modules=['staticfy', '__config__'],
      install_requires=[
          'beautifulsoup4',
      ],
      zip_safe=False)
