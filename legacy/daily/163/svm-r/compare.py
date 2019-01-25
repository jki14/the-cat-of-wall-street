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

import matplotlib.pyplot as plt

# config
nsample = 3
ntracks = 3
optionL = ['-s 3 -t 2 -g 0.000001 -c 1000000.0 -b 0 -q', '-s 3 -t 2 -g 0.000001 -c 1000000.0 -b 0 -q']
colorsL = ['r.', 'b.']

def run(tday, history):
    logstr = ''
    #
    w, x, y = history.grab(nsample, ntracks, tday+1)
    lsvmL = []
    for options in optionL:
        timer = timer_c()
        lsvmL.append(svmutil.svm_train(y, x, options))
        print 'options = %s' % (options)
        print 'svm trained successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    #
    plt.axvline(x=0.0, color='k', alpha=0.2)
    plt.axhline(y=0.0, color='k', alpha=0.2)
    for i in xrange(len(lsvmL)):
        timer = timer_c()
        p_labels, p_acc, p_vals = svmutil.svm_predict(y, x, lsvmL[i], '')
        print 'svm predicted successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
        plt.plot(p_labels, y, colorsL[i], alpha=0.5)
    plt.show()
    #
    w, x, y = history.grab(1, ntracks, tday)
    plt.axvline(x=0.0, color='k', alpha=0.2)
    plt.axhline(y=0.0, color='k', alpha=0.2)
    for i in xrange(len(lsvmL)):
        timer = timer_c()
        p_labels, p_acc, p_vals = svmutil.svm_predict(y, x, lsvmL[i], '')
        print 'svm predicted successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
        plt.plot(p_labels, y, colorsL[i], alpha=0.5)
    plt.show()

def main():
    print 'nsample = %d' % (nsample) 
    print 'ntracks = %d' % (ntracks)
    argv = sys.argv
    argc = len(argv)
    lef, rig = 0, 1
    if argc>2:
        lef = int(argv[1])
        rig = int(argv[2])
    history = history_c()
    history.load('../data/dbf/2017.dbf')
    for i in xrange(lef, rig):
        run(i, history)
        sys.stdout.flush()

if __name__ == '__main__':
    main()
