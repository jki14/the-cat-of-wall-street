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

def run(history, tweek, pref):
    #
    timer = timer_c()
    lsvm = svmutil.svm_load_model('temp.svm')
    print 'svm loaded successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    #
    w, x, y = history.grab(1, ntracks, tweek-1, pref)
    x = xfilter(x)
    timer.reset()
    p_labels, p_acc, p_vals = svmutil.svm_predict(y, x, lsvm, '')
    print 'svm predicted successfully in %s sec with %d samples.' % (str(float('{0:.3f}'.format(timer.lag()))), len(w))
    plotdraw(p_labels, y)
    #
    foo = []
    for i in xrange(len(w)):
        foo.append((w[i], p_labels[i], y[i]))
    foo.sort(key = lambda tup: (tup[1]))
    for row in foo:
        print '%s y\' = %.6f, y = %.6f' % row

def main():
    tweek = -1
    pref = ''
    try:
        tweek = int(sys.argv[1])
    except IndexError, ValueError:
        print 'error: tweek was not found.'
        return
    try:
        if sys.argv[2]!='ss':
            pref = sys.argv[2]
    except IndexError:
        pref = ''
    print 'nsample = %d' % (nsample) 
    print 'ntracks = %d' % (ntracks)
    print 'cprefix = \'%s\'' % (pref)
    history = history_c()
    history.load('../../daily/163/data/dbf/2016.dbf')
    run(history, tweek, pref)

if __name__ == '__main__':
    main()
