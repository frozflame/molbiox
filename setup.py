#!/usr/bin/env python3
# coding: utf-8

import os
import re
from setuptools import setup, find_packages, Extension
# import molbiox; exit(1)
# DO NOT import your package from your setup.py


def readfile(filename):
    with open(filename) as f:
        return f.read()


def getversion():
    root = os.path.dirname(__file__)
    with open(os.path.join(root, 'molbiox/VERSION')) as version_file:
        version = version_file.read().strip()
        regex = re.compile(r'^\d+\.\d+\.\d+$')
        if not regex.match(version):
            raise ValueError('VERSION file is corrupted')
        return version

alignlib = Extension('molbiox.lib.align', sources=['molbiox/lib/align.c'])

config = {
    'name': "molbiox",
    'version': getversion(),
    'description': "utilities for bioinformatics",
    'keywords': 'bioinformatics',
    'url': "https://github.com/frozflame/molbiox",
    'author': 'frozflame',
    'author_email': 'lendoli@163.com',
    'license': "GNU General Public License (GPL)",
    'packages': find_packages(),
    'zip_safe': False,
    'ext_modules': [alignlib],
    # namespace_packages: ["molbiox"],
    'install_requires': readfile("requirements.txt"),
    # scripts: ['bin/mbx'],
    'entry_points': {
        'console_scripts': ['mbx=molbiox.frame.command:Executor.run'],
    },
    'classifiers': [
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    # ensure copy static file to runtime directory
    'include_package_data': True,
}

setup(**config)
