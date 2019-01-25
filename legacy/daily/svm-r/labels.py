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

if '../public' not in sys.path:
    sys.path.append('../public')
from widget import timer_c
from widget import history_c

import matplotlib.pyplot as plt

# config
nsample = 5
ntracks = 5
options = '-s 3 -t 2 -g %.12f -c %.12f -b 0 -q' % (2.0**-24, 2.0**24)

def run(tday, history):
    logstr = ''
    #
    w, x, y = history.grab(nsample, ntracks, tday+1)
    timer = timer_c()
    lsvm = svmutil.svm_train(y, x, options)
    print 'svm trained successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    #
    timer = timer_c()
    w, x, y = history.grab(1, ntracks, tday)
    p_labels, p_acc, p_vals = svmutil.svm_predict(y, x, lsvm, '')
    print 'svm predicted successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    pos = np.argmax(np.array(p_labels))
    return p_labels[pos], y[pos]

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
    history.load('../data/dbf/2017.dbf')
    px = []
    py = []
    for i in xrange(lef, rig):
        rep = run(i, history)
        sys.stdout.flush()
        px.append(rep[0])
        py.append(rep[1])
    plt.axhline(y=0, color='k', alpha=0.2)
    plt.plot(px, py, 'b.')
    plt.show()

if __name__ == '__main__':
    main()
