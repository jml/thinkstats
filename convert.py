import sys

from thinkstats.fixedwidth import (
    fixed_width_to_csv,
    open_file,
    )


PREGNANCIES = {
    'path': 'data/2002FemPreg.dat.gz',
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
    }


def main():
    with open_file(PREGNANCIES['path']) as in_file:
        fixed_width_to_csv(in_file, PREGNANCIES['fields'], sys.stdout)


main()
