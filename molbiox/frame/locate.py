#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals
import os
import re

import molbiox
from molbiox.settings import all_templates

mbx_root = os.path.dirname(molbiox.__file__)


def locate_template_old(tplname):
    filename = all_templates.get(tplname, 's.script.py')
    dirpath = os.path.dirname(molbiox.__file__)
    return os.path.join(dirpath, 'templates', filename)


def locate_datafile(filename):
    return os.path.join(mbx_root, 'info', filename)


def locate_template(tplname, new=False):
    """
    Locate a template by name.
    If `new=False`, return full path of the template file;
    else, return the filename for the to-be-generated file
    :param tplname: template name, as key in `molbiox.settings.all_templates`
    :param new: if True, return the filename for the to-be-generated file
    :return: a string
    """
    filename = all_templates.get(tplname, tplname)
    if new:
        return re.sub(r'^s\.', 'run-', filename)
    dirpath = os.path.dirname(molbiox.__file__)
    return os.path.join(dirpath, 'templates', filename)