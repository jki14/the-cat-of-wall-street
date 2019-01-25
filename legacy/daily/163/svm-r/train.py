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

if '../../public' not in sys.path:
    sys.path.append('../../public')
from widget import timer_c
from widget import history_c
from widget import plotdraw 

if '../public' not in sys.path:
    sys.path.append('../public')
from xfilter import xfilter

# config
nsample = 5
ntracks = 5
options = '-s 3 -t 2 -g %.12f -c %.12f -b 0 -q' % (2.0**-24, 2.0**24)

def run(history):
    #
    w, x, y = history.grab(nsample, ntracks, 0)
    x = xfilter(x)
    timer = timer_c()
    lsvm = svmutil.svm_train(y, x, options)
    svmutil.svm_save_model('temp.svm', lsvm)
    print 'svm trained successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    #
    timer = timer_c()
    p_labels, p_acc, p_vals = svmutil.svm_predict(y, x, lsvm, '')
    print 'svm predicted successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    plotdraw(p_labels, y)

def main():
    print 'nsample = %d' % (nsample) 
    print 'ntracks = %d' % (ntracks)
    argv = sys.argv
    argc = len(argv)
    history = history_c()
    history.load('../data/dbf/2016.dbf')
    run(history)

if __name__ == '__main__':
    main()
