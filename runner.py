__author__ = 'nitinpasumarthy'

from Test import Test

trainfilepath = './data/entrain.txt'
testfilepath = './data/entest.txt'
outfilepath = './data/predictedtags.txt'

tester = Test(trainfilepath, testfilepath, outfilepath)
print("error_rate = {}".format(tester.error_rate(outfilepath, testfilepath)))
print('Done')
