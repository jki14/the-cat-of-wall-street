# -*- coding: utf-8 -*-

import json
import numpy as np
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

if '../public' not in sys.path:
    sys.path.append('../public')
from xfilter import xfilter


import matplotlib.pyplot as plt

# config
nsample = 20
ntracks = 5
options = '-s 3 -t 2 -g %.12f -c %.12f -b 0 -q' % (2.0**-3, 2.0**9)

def run(tday, history):
    logstr = ''
    #
    w, x, y = history.grab(nsample, ntracks, tday+1)
    x = xfilter(x)
    timer = timer_c()
    lsvm = svmutil.svm_train(y, x, options)
    #svmutil.svm_save_model('benchmark.svm', lsvm)
    #lsvm = svmutil.svm_load_model('benchmark.svm')
    print 'svm trained successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    #
    timer = timer_c()
    w, x, y = history.grab(1, ntracks, tday)
    x = xfilter(x)
    p_labels, p_acc, p_vals = svmutil.svm_predict(y, x, lsvm, '')
    print 'svm predicted successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    foo = []
    for i in xrange(len(y)):
        foo.append((p_labels[i], y[i]))
    foo.sort(key = lambda tup: (-tup[0]))
    return [row[1] for row in foo]

def main():
    print 'nsample = %d' % (nsample) 
    print 'ntracks = %d' % (ntracks)
    print 'options = %s' % (options)
    argv = sys.argv
    argc = len(argv)
    lef, rig = 0, 1
    if argc>2:
        lef = int(argv[1])
        rig = int(argv[2])
    history = history_c()
    history.load('../data/dbf/2016.dbf')
    px = []
    py = [[], [], []]
    pc = ['r.', 'b.', 'g.']
    for i in xrange(lef, rig):
        rep = run(i, history)
        sys.stdout.flush()
        px.append(i)
        for k in xrange(3):
            py[k].append(rep[k])
    plt.axhline(y=0.0, color='k', alpha=0.2)
    for k in xrange(3):
        mean = np.array(py[k]).mean()
        print 'pos %d, mean = %.12f' % (k, mean)
        plt.plot(px, py[k], pc[k])
        plt.axhline(y=mean, color=pc[k][:-1], alpha=0.3)
    sys.stdout.flush()
    plt.show()

if __name__ == '__main__':
    main()
