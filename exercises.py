from thinkstats.funky import dichotomy
from thinkstats.stats import mean, std_dev
from thinkstats.survey import load_records, PREGNANCIES, select


def summarize(title, xs):
    print title
    xs = list(xs)
    print 'mean: %s' % mean(xs)
    print 'std dev: %s' % std_dev(xs)
    print


def first():
    pregnancies = list(load_records(**PREGNANCIES))
    live_births = [rec for rec in pregnancies if rec['outcome'] == 1]
    rest, firstborns = dichotomy(lambda rec: rec['birthord'] == 1, live_births)
    summarize('First borns', select(firstborns, 'prglength'))
    summarize('Other births', select(rest, 'prglength'))


first()
