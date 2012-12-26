from thinkstats.funky import dichotomy
from thinkstats.stats import mean
from thinkstats.survey import load_records, PREGNANCIES, select


def summarize(xs):
    xs = list(xs)
    print 'mean: %s' % mean(xs)


def first():
    pregnancies = list(load_records(**PREGNANCIES))
    live_births = [rec for rec in pregnancies if rec['outcome'] == 1]
    rest, firstborns = dichotomy(lambda rec: rec['birthord'] == 1, live_births)
    summarize(select(firstborns, 'prglength'))
    summarize(select(rest, 'prglength'))


first()
