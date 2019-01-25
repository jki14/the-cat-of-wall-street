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
ntracks = 60
options = '-s 3 -t 2 -g %.24f -c %.24f -b 0 -q' % (2.0**-60, 2.0**30)

def run(tweek, history, logfile):
    logstr = ''
    #
    w, x, y = history.grab(nsample, ntracks, tweek+1)
    x = xfilter(x)
    timer = timer_c()
    lsvm = svmutil.svm_train(y, x, options)
    #svmutil.svm_save_model('benchmark.svm', lsvm)
    #lsvm = svmutil.svm_load_model('benchmark.svm')
    print 'svm trained successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    #
    timer = timer_c()
    p_labels, p_acc, p_vals = svmutil.svm_predict(y, x, lsvm, '')
    print 'svm predicted successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    plotdraw(p_labels, y)
    #
    timer = timer_c()
    w, x, y = history.grab(1, ntracks, tweek)
    x = xfilter(x)
    p_labels, p_acc, p_vals = svmutil.svm_predict(y, x, lsvm, '')
    print 'svm predicted successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    plotdraw(p_labels, y)
    #foo = []
    #for i in xrange(len(w)):
    #    foo.append((w[i], p_labels[i], y[i]))
    #foo.sort(key = lambda tup: (tup[1]))
    #for row in foo:
    #    print '%s y\' = %.6f, y = %.6f' % row

def main():
    print 'nsample = %d' % (nsample) 
    print 'ntracks = %d' % (ntracks)
    print 'options = %s' % (options)
    argv = sys.argv
    argc = len(argv)
    lef, rig, logfile = 0, 1, 'benchmark.log'
    if argc>2:
        lef = int(argv[1])
        rig = int(argv[2])
        #logfile = argv[3]
    #with open(logfile, 'a') as log:
    #    log.write('nsample = %d\nntracks = %d\noptions = %s\n' % (nsample, ntracks, options))
    history = history_c()
    history.load('../../daily/163/data/dbf/2016.dbf')
    for i in xrange(lef, rig):
        run(i, history, logfile)
        sys.stdout.flush()

if __name__ == '__main__':
    main()
