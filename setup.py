#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup, find_packages


def readfile(filename):
    with open(filename) as f:
        return f.read()


setup(
    name="molbiox",
    version="0.0.6",
    description="utilities for bioinformatics",
    keywords='bioinformatics',
    url="https://github.com/frozflame/molbiox",
    author='frozflame',
    author_email='lendoli@163.com',
    license="GNU General Public License (GPL)",
    packages=find_packages(),
    zip_safe=False,
    # namespace_packages=["molbiox"],
    install_requires=readfile("requirements.txt"),
    # scripts=['bin/mbx'],
    entry_points={
        'console_scripts': ['mbx=molbiox.frame.command:Executor.run'],
    },
    classifiers=[
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    # ensure copy static file to runtime directory
    include_package_data=True,
)

