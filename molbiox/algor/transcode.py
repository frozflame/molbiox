#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import numpy as np

import molbiox.kb.transcode
from molbiox.kb import translate


class CharsMapper(object):
    def __init__(self, config):
        self.refarr = self._build_mapping_array(**config)

    @staticmethod
    def _build_mapping_array(src, dest, outlier='-'):
        if not len(src) == len(dest):
            raise ValueError('lengths of src and dst must be equal')

        sarr = np.fromstring(src, dtype='uint8')
        darr = np.fromstring(dest, dtype='uint8')

        arr = np.zeros(256, dtype='uint8')
        arr[sarr] = darr
        arr[arr == 0] = ord(outlier)
        return arr

    @classmethod
    def create_mapper_compl_dna(cls):
        return cls(molbiox.kb.transcode.complDNA)

    @classmethod
    def create_mapper_compl_rna(cls):
        return cls(molbiox.kb.transcode.complRNA)

    def transcode(self, string):
        iarr = np.fromstring(string, dtype='uint8')
        arr = self.refarr[iarr]
        return arr.tostring()   # returning bytes

