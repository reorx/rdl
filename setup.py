#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup


package_name = 'rdl'


def get_version():
    import ast

    def parse_version(f):
        for line in f:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s

    for i in [package_name + '/__init__.py', package_name + '.py']:
        try:
            with open(i, 'r') as f:
                return parse_version(f)
        except IOError:
            pass


def get_long_description():
    try:
        with open('README.rst', 'r') as f:
            return f.read()
    except IOError:
        return ''


setup(
    name=package_name,
    version=get_version(),
    author='reorx',
    url='https://github.com/reorx/rdl',
    description='Redis dump & load tool.',
    long_description=get_long_description(),
    license='License :: OSI Approved :: MIT License',
    py_modules=['rdl'],
    install_requires=[
        'redis>=2.9'
    ],
    entry_points={
        'console_scripts': [
            'rdl = rdl:main',
        ]
    },
)
