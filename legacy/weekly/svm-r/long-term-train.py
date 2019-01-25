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
nsample = 100
ntracks = 20
options = '-s 3 -t 2 -g %.24f -c %.24f -b 0 -q' % (2.0**-24, 2.0**24)

def run(history, tweek, pref):
    #
    w, x, y = history.grab(nsample, ntracks, tweek, pref)
    x = xfilter(x)
    timer = timer_c()
    lsvm = svmutil.svm_train(y, x, options)
    svmutil.svm_save_model('long-term.svm', lsvm)
    print 'svm trained successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    #
    timer = timer_c()
    p_labels, p_acc, p_vals = svmutil.svm_predict(y, x, lsvm, '')
    print 'svm predicted successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    plotdraw(p_labels, y)

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
    history.load('../../daily/163/data/dbf/2012.dbf')
    run(history, tweek, pref)

if __name__ == '__main__':
    main()
