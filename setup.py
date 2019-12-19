#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) The cliform project

import codecs
import os
import re

from setuptools import find_packages, setup

root_dir = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = 'src'


def get_version(src_dir, package_name):
    version_re = re.compile(r"^__version__ = [\"']([\w_.-]+)[\"']$")
    init_path = os.path.join(root_dir, src_dir, package_name, '__init__.py')
    with codecs.open(init_path, 'r', 'utf-8') as f:
        for line in f:
            match = version_re.match(line[:-1])
            if match:
                return match.groups()[0]
    return '0.1.0'


PACKAGE = 'cliform'


setup(
    name=PACKAGE,
    version=get_version(SRC_DIR, PACKAGE),
    author="Raphaël Barrois",
    author_email="raphael.barrois+cliform@polytechnique.org",
    description="Convert a Django Form to an interactive command line prompt.",
    long_description=''.join(open('README.rst', 'r', encoding='utf-8').readlines()),
    license='BSD',
    keywords=['django', 'form', 'cli', 'command line', 'form', 'prompt', 'cliform'],
    url='https://github.com/rbarrois/cliform',
    download_url='http://pypi.python.org/pypi/cliform/',
    packages=find_packages(SRC_DIR),
    package_dir={
        '': SRC_DIR,
    },
    install_requires=[
        'Django>=2.0',
    ],
    python_requires='>=3.7',
    setup_requires=[
        'setuptools>=0.8',
    ],
    zip_safe=False,
    tests_require=[
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Terminals",
    ],
)
