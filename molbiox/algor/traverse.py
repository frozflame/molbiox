#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import six


class Reg(type):
    # function => registed types set ([int, float])
    __handlers__ = dict()

    def __init__(cls, name, bases, dic):

        super(Reg, cls).__init__(name, bases, dic)
        if not hasattr(cls, 'handlers'):
            cls.handlers = dict()

        # exclude `object`
        mro = cls.mro()[:-1]
        # reverse order: ancester first, decedents override
        mro.reverse()
        for t in mro:
            # all methods
            meths = (v for v in t.__dict__.values() if hasattr(v, '__call__'))
            for m in meths:
                if m in cls.__handlers__:
                    for typ in cls.__handlers__[m]:
                        cls.handlers[typ] = m

    @classmethod
    def register_handler(mcs, *types):
        def decorator(func):
            mcs.__handlers__[func] = types
            return func
        return decorator


@six.add_metaclass(Reg)
class Traverser(object):

    handlers = dict()

    def __init__(self, obj, consumer):
        self.queue = six.moves.queue.Queue()
        self.queue.put(obj)
        self.consumer = consumer

    def traverse(self):
        while not self.queue.empty():
            obj = self.queue.get()
            for typ in obj.__class__.mro():
                if typ in self.handlers:
                    self.handlers[typ](self, obj)

    @Reg.register_handler(int, float, str, bytes)
    def handle_primatives(self, obj):
        s = '<{}:{}>'.format(obj.__class__.__name__, obj)
        self.consumer(s)

    @Reg.register_handler(set)
    def handle_set(self, obj):
        self.consumer('<set>')
        items = list(obj)
        items.sort()
        for item in items:
            self.queue.put(item)

    @Reg.register_handler(list)
    def handle_list(self, obj):
        self.consumer('<list>')
        for item in obj:
            self.queue.put(item)

    @Reg.register_handler(dict)
    def handle_dict(self, obj):
        self.consumer('<dict>')
        keys = list(obj)
        keys.sort()
        for k in keys:
            self.queue.put(k)
            self.queue.put(obj[k])

    # the last resort
    @Reg.register_handler(object)
    def handle_object(self, _):
        self.consumer('<object>')
