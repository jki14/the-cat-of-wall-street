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
from widget import plotdraw

# config
nsample = 5
ntracks = 5
options = '-s 3 -t 2 -g %.12f -c %.12f -b 0 -q'

def run(tday, history, pg, pc):
    #
    w, x, y = history.grab(nsample, ntracks, tday+1)
    lsvm = svmutil.svm_train(y, x, options % (pg, pc))
    #
    w, x, y = history.grab(1, ntracks, tday)
    p_labels, p_acc, p_vals = svmutil.svm_predict(y, x, lsvm, '')
    #
    ase = np.square(np.array(p_labels) - np.array(y)).sum()
    mse = np.square(np.array(p_labels) - np.array(y)).mean()
    print '[%s] => (%.12f)' % (options % (pg, pc), mse)
    sys.stdout.flush()
    return ase, len(p_labels)

def main():
    print 'nsample = %d' % (nsample) 
    print 'ntracks = %d' % (ntracks)
    sys.stdout.flush()
    argv = sys.argv
    argc = len(argv)
    lef, rig = 0, 1
    if argc>2:
        lef = int(argv[1])
        rig = int(argv[2])
    history = history_c()
    history.load('../data/dbf/2017.dbf')
    report = []
    for pgy in xrange(-30, 30, 6):
        row = []
        for pcy in xrange(-30, 30, 6):
            acc = 0.0
            num = 0.0
            for i in xrange(lef, rig):
                foo = run(i, history, 2.0**pgy, 2.0**pcy)
                acc += foo[0]
                num += foo[1]
            row.append(acc/num)
        report.append(row)
    print report

if __name__ == '__main__':
    main()
