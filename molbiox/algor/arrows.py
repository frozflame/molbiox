#!/usr/bin/env python3
# coding: utf-8
from __future__ import unicode_literals, print_function
import numpy as np


class ArrowCalculator(object):

    def __init__(self, alpha=.7, beta=1., height1=24, height2=32):
        cot = lambda x: 1./np.tan(x)
        self.alpha = alpha
        self.beta = beta
        self.height1 = height1
        self.height2 = height2
        self.threshold1 = height2 * (cot(alpha) - cot(beta))
        self.threshold2 = self.threshold1 + height1 * cot(beta)

    def calc(self, length):
        """
        For understanding of the formula
        Not intended for actual use
        :param length:
        :return:
        """
        data = np.empty([8, 2])
        tan = np.tan
        cot = lambda x: 1./np.tan(x)

        if length > self.threshold2:
            data[0] = 0, 0
            data[1] = self.height2 * cot(self.alpha), self.height1
            data[2] = 0, length - self.threshold2
            data[3] = length, self.height1

        elif self.threshold1 < length < self.threshold2:
            data[0] = 0, 0
            data[1] = self.height2 * cot(self.alpha), self.height1
            data[2] = length, (length-self.threshold1) * tan(self.beta)
            data[3] = length, (length-self.threshold1) * tan(self.beta)
        else:
            data[0] = 0, 0
            data[1] = self.height2 * cot(self.alpha), self.height1
            data[2] = length, 0
            data[3] = length, 0

        data[5:8] = data[1:4][::-1] * np.array([1, -1])
        return data

    def calculate(self, lengths):
        """
        :param lengths: 1d array
        :return:
        """
        data = np.zeros([len(lengths), 8, 2])
        tan = np.tan
        cot = lambda x: 1./np.tan(x)

        # data[:, 0, :] = 0, 0
        data[:, 1, :] = self.height2 * cot(self.alpha), self.height1

        mask_th2a = lengths < self.threshold2
        mask_th2b = lengths > self.threshold2
        mask_th1b = lengths > self.threshold1

        data[:, 2, 0][mask_th2a] = lengths[mask_th2a]

        data[:, 2, 1][mask_th1b] = ((lengths-self.threshold1) * tan(self.beta))[mask_th1b]

        data[:, 2, 1][mask_th2b] = (lengths - self.threshold2)[mask_th2b]

        data[:, 3, 0] = lengths
        data[:, 3, 1][mask_th1b] = ((lengths-self.threshold1) * tan(self.beta))[mask_th1b]

        data[:, 3, 1][mask_th2b] = self.height1

        data[:, 5:8, :] = data[:, 1:4, :][:, ::-1, :] * np.array([1, -1])
        return data

    def make(self, arr):
        """
        :param arr: 1d or 2d array
        """
        if not isinstance(arr, np.ndarray):
            arr = np.array(arr)
        if arr.ndim > 2:
            raise ValueError("number of dimensions of 'arr' should be 1 or 2")

        # simply an array of lengths
        if arr.ndim == 1 or arr.shape[-1] == 1:
            return self.calculate(arr.reshape([-1]))

        # treat last dim as (start, end)
        if arr.shape[-1] == 2:
            lengths = arr[:, 1] - arr[:, 0]
            data = self.calculate(lengths)
            data[:, :, 0:1] += arr[:, 0].reshape([-1, 1, 1])
            return data

        # treat last dim as (x_start, x_end, y)
        if arr.shape[-1] == 3:
            data = self.make(arr[:, :2])
            data[:, :, 1] += arr[:, 2].reshape([-1, 1, 1])
            return data


arrow_anatomy = """
Anatomy of an Arrow
by Hailong on 2015 Xmas

                           /+ 1                     +
                         / /                        |
                       /  /                         |
                     /   /                          |
                   /    /                           |
                 /     /                            | < height2
               /      /                             |
             /       / <beta                    3   |
           /      2 +---------------------------+   |      +
         / <alpha  /                            |   |      |  < height1
     0  <---------+-----------------------------+   +      +
         \         \                            |              alpha < beta
           \      . 5---------------------------+            height1 < height2
                  . .                           4
                  . .
                  . .
        + - - - - +     threshold1
        + - - - - - +   threshold2

        + < - - - - - - length  - - - - - - - > +



length is the main variable.
alpha, height2 are always constant

Threshold 2
As length decreases, point2 and point3 will join, and height1 begin to decrease.

Threshold 1
As length decreases continuously, height1 will become 0, and beta begin to decrease.
"""