__author__ = 'nitinpasumarthy'

from Train import Train
from Tagger import Tagger

t = Train('./data/entrain.txt')
s = """When
such
claims
and
litigation
extend
beyond
the
period
,
the
syndicates
can
extend
their
accounting
deadlines
."""
tg = Tagger(t, s)
print tg.tag()
print('Done')