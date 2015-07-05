#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup, find_packages


def readfile(filename):
    with open(filename) as f:
        return f.read()


setup(
    name="molbiox",
    version="0.0.1",
    packages=find_packages(),
    zip_safe=False,
    namespace_packages=["molbiox"],
    install_requires=readfile("requirements.txt"),

    # ensure copy static file to runtime directory
    include_package_data=True,
)

