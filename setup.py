#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup, find_packages


def readfile(filename):
    with open(filename) as f:
        return f.read()


setup(
    name="molbiox",
    version="0.0.3",
    description="utilities for bioinformatics",
    url="https://github.com/frozflame/molbiox",
    author='frozflame',
    author_email='lendoli@163.com',
    license="GNU General Public License (GPL)",
    packages=find_packages(),
    zip_safe=False,
    # namespace_packages=["molbiox"],
    install_requires=readfile("requirements.txt"),

    # ensure copy static file to runtime directory
    include_package_data=True,
)

