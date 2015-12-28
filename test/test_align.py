#!/usr/bin/env python3
# coding: utf-8
from __future__ import unicode_literals, print_function
import time
import numpy as np
from molbiox.algor.align import Aligner
from molbiox.algor.align import format
from molbiox.io import submatrix, fasta
from molbiox.frame import iteration

path = 'data/rmlA.2x.fa'
score_type = 'int64'


def test():
    import numpy as np
    path_submatrix = '/Users/Hailong/Downloads/pam250.txt'
    istring, jstring, scores = submatrix.read(path_submatrix)

    submarix = np.array(scores).astype(score_type)
    ali = Aligner.from_submatrix(istring, jstring, submarix)

    iseq, jseq = fasta.read(path, castfunc=lambda x: [s.seq for s in x])

    t = time.time()
    for i in range(1000):
        matrx, istring, jstring = ali.align(iseq, jseq, backtrack=True)
    print('time:', time.time() - t)

    mstring = format.match(istring, jstring)

    for items in iteration.chunkwise(60, istring, mstring, jstring):
        print('\n'.join(items), end='\n\n')

    # debug.show_path(matrx)

x = test()


def test2():
    table = np.identity(256, dtype=np.int64)
    table[0, 0] = 0
    table.shape = -1
    import ctypes
    from numpy.ctypeslib import ndpointer
    lib = ctypes.cdll.LoadLibrary(libpath)
    fun = lib.build
    fun.argtypes = [
        ndpointer(ctypes.c_int64, flags="C_CONTIGUOUS"),
        ctypes.c_int,   # isize
        ctypes.c_int,   # jsize
        ctypes.c_int,   # rho
        ctypes.c_int,   # sigma
        ctypes.c_uint,  # local_
    ]
    s = 'christmas'
    l = len(s) + 1
    matr = build_matr(s, s, table)
    matr <<= 2
    print(matr[..., 2])
    matr[0, :, :] = 0
    matr[:, 0, :] = 0
    matr[:, :, 0] = 0
    matr[:, :, 1] = 0
    fun(matr, l, l, 0, 0, 0)
    return matr


data = np.array([[0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 1],
                 [0, 1, 0, 0, 1],
                 [0, 1, 0, 0, 1],
                 [0, 0, 1, 1, 0],
                 [0, 0, 1, 1, 0]])

