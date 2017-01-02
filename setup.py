#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.1.0'

from setuptools import setup

with open('README.rst', 'r') as f:
    desc = f.read()

setup(
    name='rdl',
    version=__version__,
    author='reorx',
    url='http://github.com/reorx/rdl',
    description='Redis dump & load tool.',
    long_description=desc,
    py_modules=['rdl'],
    entry_points={
        'console_scripts': [
            'rdl = rdl:main',
        ]
    },
    install_requires=[
        'redis>=2.9'
    ],
)
