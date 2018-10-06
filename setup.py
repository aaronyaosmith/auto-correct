# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ac',
    version='0.1',
    description='CUAir spell checker',
    long_description=readme,
    author='Aaron Yao-Smith',
    author_email='aty25@cornell.edu',
    url='https://github.com/aaronyaosmith/auto-correct',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
