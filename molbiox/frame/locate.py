#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals
import os
import molbiox
from molbiox.settings import all_templates

__author__ = 'Hailong'

mbx_root = os.path.dirname(molbiox.__file__)


def locate_template(tplname):
    filename = all_templates.get(tplname, 's.script.py')
    dirpath = os.path.dirname(molbiox.__file__)
    return os.path.join(dirpath, 'templates', filename)


def locate_datafile(filename):
    return os.path.join(mbx_root, 'info', filename)

