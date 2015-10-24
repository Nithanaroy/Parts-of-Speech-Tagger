__author__ = 'nitinpasumarthy'

from Train import Train

t = Train('./data/entrain.txt')
t.compute_a_and_b()
print('Done')