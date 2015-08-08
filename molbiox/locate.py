#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals
import os
import molbiox

__author__ = 'Hailong'

mbx_root = os.path.dirname(molbiox.__file__)

def locate_template(filename):
    return os.path.join(mbx_root, 'template', filename)


def locate_datafile(filename):
    return os.path.join(mbx_root, 'info', filename)

