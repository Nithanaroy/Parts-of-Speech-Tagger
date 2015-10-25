__author__ = 'nitinpasumarthy'

from Test import Test

filepath = './data/entrain.txt'
outfilepath = './data/predictedtags.txt'

Test(filepath, filepath, outfilepath)
print('Done')
