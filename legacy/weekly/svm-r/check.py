# -*- coding: utf-8 -*-

import json
import numpy
import os
import sys
import time

libsvm_path = os.path.expanduser('~')+'/libs/libsvm-3.22/python'
if libsvm_path not in sys.path:
    sys.path.append(libsvm_path)
import svmutil

if '../public' not in sys.path:
    sys.path.append('../public')
from widget import timer_c
from widget import history_c
from widget import plotdraw 
from xfilter import xfilter

# config
nsample = 4
ntracks = 20
options = '-s 3 -t 2 -g %.24f -c %.24f -b 0 -q' % (2.0**-24, 2.0**24)

def run(history, tweek, pref):
    #
    w, x, y = history.grab(nsample, ntracks, tweek, pref)
    x = xfilter(x)
    timer = timer_c()
    lsvm = svmutil.svm_train(y, x, options)
    #print 'svm trained successfully in %s sec with %d samples.' % (str(float('{0:.3f}'.format(timer.lag()))), len(w))
    #
    w, x, y = history.grab(1, ntracks, tweek-1, pref)
    x = xfilter(x)
    timer.reset()
    p_labels, p_acc, p_vals = svmutil.svm_predict(y, x, lsvm, '')
    #print 'svm predicted successfully in %s sec with %d samples.' % (str(float('{0:.3f}'.format(timer.lag()))), len(w))
    #
    foo = []
    for i in xrange(len(w)):
        foo.append((w[i], p_labels[i], y[i]))
    foo.sort(key = lambda tup: (-tup[1]))
    for i in xrange(3):
        print '%s y\' = %.6f, y = %.6f' % foo[i]

def main():
    print 'nsample = %d' % (nsample) 
    print 'ntracks = %d' % (ntracks)
    sys.stdout.flush()
    earliest = -1
    try:
        earliest = int(sys.argv[1])
    except IndexError, ValueError:
        print 'error: tweek was not found.'
        return
    history = history_c()
    history.load('../../daily/163/data/dbf/2016.dbf')
    uniws = history.uniws()
    for tweek in xrange(earliest+1):
        if tweek>0:
            print uniws[tweek-1]
        else:
            print '?:??????:????-??-??:(?)'
        sys.stdout.flush()
        run(history, tweek, '')
        sys.stdout.flush()
        run(history, tweek, 'sh')
        sys.stdout.flush()

if __name__ == '__main__':
    main()
