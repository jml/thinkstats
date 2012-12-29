"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""


from pprint import pprint

from thinkstats.funky import identity


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


def select(records, column):
    return (record[column] for record in records)


def get_birthweight(record):
    lb = record['birthwgt_lb']
    oz = record['birthwgt_oz']
    if lb and lb < 20 and oz and oz <= 16:
        return lb * 16 + oz
