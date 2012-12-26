"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import gzip
import os

from pprint import pprint

from thinkstats.funky import identity


def get_data_path(path):
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'data', path)


def open_file(path):
    """Open file at 'path', decompressing if needed."""
    if path.endswith('.gz'):
        return gzip.open(path)
    else:
        return open(path)


def parse_line(fields, line):
    parsed = {}
    for (name, start, end, parser) in fields:
        value = None
        field = line[start - 1:end].strip()
        if field:
            try:
                value = parser(field)
            except ValueError:
                raise ValueError("Could not parse field %r: %r" % (name, field))
        parsed[name] = value
    return parsed


OUTCOME_LABELS = {
    1: 'LIVE BIRTH',
    2: 'INDUCED ABORTION',
    3: 'STILLBIRTH',
    4: 'MISCARRIAGE',
    5: 'ECTOPIC PREGNANCY',
    6: 'CURRENT PREGNANCY',
    }


def recode(rec):
    # divide mother's age by 100
    if rec['agepreg']:
        rec['agepreg'] /= 100.0
    # convert weight at birth from lbs/oz to total ounces
    # note: there are some very low birthweights
    # that are almost certainly errors, but for now I am not
    # filtering
    rec['totalwgt_oz'] = get_birthweight(rec)
    return rec


PREGNANCIES = {
    'path': '2002FemPreg.dat.gz',
    'fields': [
        ('caseid', 1, 12, int),
        ('nbrnaliv', 22, 22, int),
        ('babysex', 56, 56, int),
        ('birthwgt_lb', 57, 58, int),
        ('birthwgt_oz', 59, 60, int),
        ('prglength', 275, 276, int),
        ('outcome', 277, 277, int),
        ('birthord', 278, 279, int),
        ('agepreg', 284, 287, int),
        ('finalwgt', 423, 440, float),
        ],
    'recoder': recode,
    }


def load_records(path, fields, recoder=identity):
    with open_file(get_data_path(path)) as f:
        for line in f:
            yield recoder(parse_line(fields, line))


def select(records, column):
    return (record[column] for record in records)


def get_birthweight(record):
    lb = record['birthwgt_lb']
    oz = record['birthwgt_oz']
    if lb and lb < 20 and oz and oz <= 16:
        return lb * 16 + oz


if __name__ == '__main__':
    pregs = load_records(**PREGNANCIES)
    for preg in pregs:
        pprint(recode(preg))
