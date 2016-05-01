#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import itertools
from collections import OrderedDict
from jinja2 import Template

from molbiox.frame import streaming, interactive
from molbiox.frame.environ import locate_template


def render_primer3_input(**kwargs):
    tpl_path = locate_template('d.primer3.txt')
    tpl = open(tpl_path).read()
    tpl = Template(tpl)
    return tpl.render(**kwargs)


@interactive.castable
def read_boulder(infile):
    """
    Read a boulder-io file as dict objects
    :param infile:
    :return: a generator of dict objects
    """
    with streaming.FileAdapter(infile, 'r') as fila:
        fila_lines = (l.strip() for l in fila if '=' in l)
        fila_lines = itertools.chain(fila_lines, ['='])

        record = dict()
        for l in fila_lines:
            # record terminated by '='
            if l == '=' and record:
                yield record
                record = dict()
            else:
                key, val = l.split('=', maxsplit=1)
                record[key.strip().lower()] = val.strip()


@interactive.castable
def format_table(records):
    # make a copy of records, in case of one-off iterable/generator
    records = list(records)

    def _get_column_widths(records, keys):
        widths = dict()
        for r in records:
            for k in keys:
                length = len(r.get(k, ''))
                if length > widths.get(k, 0):
                    widths[k] = length
        return widths

    adjustments = OrderedDict([
        ('sequence_id',
            lambda s, n: s.ljust(n)),
        ('primer_left_0_sequence',
            lambda s, n: s.ljust(n)),
        ('primer_right_0_sequence',
            lambda s, n: s.ljust(n)),
        ('primer_internal_0_sequence',
            lambda s, n: s.ljust(n)),
        ('primer_left_0',
            lambda s, n: s.split(',')[0].rjust(n)),
        ('primer_right_0',
            lambda s, n: s.split(',')[0].rjust(n)),
        ('primer_internal_0',
            lambda s, n: s.split(',')[0].rjust(n)),
        ('primer_pair_0_product_size',
            lambda s, n: s.rjust(n))
    ])

    widths = _get_column_widths(records, adjustments)

    for r in records:
        if r.get('primer_error', ''):
            continue
        items = []
        for k in adjustments:
            x = adjustments[k](r.get(k, '_'), widths.get(k, 0))
            items.append(x)
        yield ' '.join(items)

table_header = {
    'sequence_id':	                '#id',
    'primer_left_0_sequence':	    'primerLeft',
    'primer_right_0_sequence':	    'primerRight',
    'primer_internal_0_sequence':	'interalOligo',
    'primer_left_0':	            'posL',
    'primer_right_0':	            'posR',
    'primer_internal_0':	        'posI',
    'primer_pair_0_product_size':	'productSize',
}
