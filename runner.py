__author__ = 'nitinpasumarthy'

from Test import Test

trainfilepath = './data/entrain.txt'
testfilepath = './data/entest.txt'
outfilepath = './data/predictedtags.txt'

Test(trainfilepath, testfilepath, outfilepath)
print('Done')
