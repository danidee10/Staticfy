#!/usr/bin/env python

from setuptools import setup

setup(name='Staticfy',
      version='1.1',
      description='Convert static assets links to dynamic web framework links',
      url='https://github.com/danidee10/Staticfy',
      author='Osaetin Daniel',
      author_email='osaetindaniel@gmail.com',
      license='GPL',
      entry_points={
        'console_scripts': ['staticfy = staticfy.staticfy:main']
      },
      packages=['staticfy'],
      install_requires=[
          'beautifulsoup4',
      ],
      zip_safe=False)
