#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import numpy as np
from molbiox.frame import compat


tan = np.tan
cot = lambda x: 1./np.tan(x)


class ArrowCalc(object):

    def __init__(self, alpha=.7, beta=1., height1=16, height2=32):
        self.alpha = alpha
        self.beta = beta
        self.height1 = height1
        self.height2 = height2
        self.threshold1 = height2 * (cot(alpha) - cot(beta))
        self.threshold2 = self.threshold1 + height1 * cot(beta)

    def __call__(self, arr):
        return self.calc(arr)

    def prototype(self, length):
        """
        For understanding of the formula
        Not intended for actual use
        :param length:
        :return:
        """
        data = np.empty([8, 2])
        if length >= self.threshold2:
            data[1] = self.height2 * cot(self.alpha), self.height2
            data[2] = self.threshold2, self.height1
            data[3] = length, self.height1

        elif self.threshold1 < length < self.threshold2:
            data[1] = self.height2 * cot(self.alpha), self.height2
            data[2] = length, (length-self.threshold1) * tan(self.beta)
            data[3] = length, (length-self.threshold1) * tan(self.beta)
        else:
            data[1] = self.height2 * cot(self.alpha), self.height2
            data[2] = length, 0
            data[3] = length, 0

        data[4:7] = data[1:4][::-1] * np.array([1, -1])
        data[0] = 0, 0
        data[7] = 0, 0
        return data

    def calculate(self, lengths):
        """
        Algorithm
        :param lengths: 1d array, all values should be positive
        :return:
        """
        data = np.zeros([len(lengths), 8, 2])

        # point 0 is (0, 0)
        # dt[:, 0, 0] = 0
        # dt[:, 0, 1] = 0

        # point 1 is fixed
        data[:, 1, 0] = self.height2 * cot(self.alpha)
        data[:, 1, 1] = self.height2

        # masks
        mask0 = lengths <= self.threshold1
        mask1 = (self.threshold1 < lengths) & (lengths < self.threshold2)
        mask2 = lengths >= self.threshold2

        data[:, 2, 0][mask0] = lengths[mask0]
        data[:, 2, 0][mask1] = lengths[mask1]
        data[:, 2, 0][mask2] = self.threshold2

        data[:, 3, 0] = lengths

        # point 2 and point 3 are of same height
        # dt[:, 2, 1][mask0] = 0
        # dt[:, 3, 1][mask0] = 0
        data[:, 2, 1][mask1] = ((lengths-self.threshold1) * tan(self.beta))[mask1]
        data[:, 3, 1][mask1] = ((lengths-self.threshold1) * tan(self.beta))[mask1]
        data[:, 2, 1][mask2] = self.height1
        data[:, 3, 1][mask2] = self.height1

        data[:, 4:7, :] = data[:, 1:4, :][:, ::-1, :] * np.array([1, -1])
        return data

    def calc(self, arr):
        """
        You should use this instead of 'calculate'
        :param arr: 1d or 2d array
        """
        arr = compat.make_array(arr)

        if arr.ndim > 2:
            raise ValueError("number of dimensions of 'arr' should be 1 or 2")

        # simply an array of lengths
        if arr.ndim == 1 or arr.shape[-1] == 1:
            lengths = arr.reshape([-1])
            orients = np.sign(lengths)
            results = self.calculate(np.abs(lengths))
            results[:, :, 0] *= orients.reshape([-1, 1])
            return results

        # treat last dim as (start, end)
        if arr.shape[-1] == 2:
            lengths = arr[:, 0] - arr[:, 1]
            orients = np.sign(lengths)  # length can NOT be 0
            results = self.calculate(abs(lengths))
            results[:, :, 0] *= orients.reshape([-1, 1])
            results[:, :, 0] += arr[:, 1].reshape([-1, 1])
            return results

        # treat last dim as (x_start, x_end, y)
        if arr.shape[-1] == 3:
            results = self.calc(arr[:, :2])
            results[:, :, 1] += arr[:, 2].reshape([-1, 1])
            return results


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