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
from xfilter import xfilter

import matplotlib.pyplot as plt

# config
nsample = 16
ntracks = 80
options = '-s 3 -t 2 -g %.24f -c %.24f -b 0 -q' % (2.0**-24, 2.0**24)

def run(history, tweek, pref, selections):
    logstr = ''
    #
    w, x, y = history.grab(nsample, ntracks, tweek+1, pref, 180, 90, 80000)
    x = xfilter(x)
    timer = timer_c()
    lsvm = svmutil.svm_train(y, x, options)
    #svmutil.svm_save_model('benchmark.svm', lsvm)
    #lsvm = svmutil.svm_load_model('benchmark.svm')
    print 'svm trained successfully in %s sec with %d samples.' % (str(float('{0:.3f}'.format(timer.lag()))), len(w))
    #
    timer = timer_c()
    w, x, y = history.grab(1, ntracks, tweek, pref, 180, 90, 80000)
    x = xfilter(x)
    p_labels, p_acc, p_vals = svmutil.svm_predict(y, x, lsvm, '')
    print 'svm predicted successfully in %s sec with %d samples.' % (str(float('{0:.3f}'.format(timer.lag()))), len(w))
    foo = []
    for i in xrange(len(y)):
        foo.append((p_labels[i], y[i], w[i]))
    foo.sort(key = lambda tup: (-tup[0]))
    selections['code'].append(foo[0][2])
    selections['tweek'].append(tweek)
    return [row[1] for row in foo]

def main():
    notes = 'nsample = %d\n' % (nsample)
    print 'nsample = %d' % (nsample)
    notes += 'ntracks = %d\n' % (ntracks)
    print 'ntracks = %d' % (ntracks)
    notes += 'options = %s\n' % (options)
    print 'options = %s' % (options)
    argv = sys.argv
    argc = len(argv)
    lef, rig = 0, 1
    pref = ''
    img = 'untitled.png'
    if argc>2:
        lef = int(argv[1])
        rig = int(argv[2])
    if argc>3 and argv[3]!='ss':
        pref = argv[3]
    if argc>4:
        img = argv[4]
    notes += 'cprefix = \'%s\'\n' % (pref)
    print 'cprefix = \'%s\'' % (pref)
    history = history_c()
    #history.load('../../daily/163/data/dbf/2016.dbf')
    history.load('../../daily/163/data/dbf/2012.dbf')
    selections = {'code':[], 'tweek':[]}
    px = []
    py = [[], [], []]
    pc = ['r.', 'b.', 'g.']
    for i in xrange(lef, rig):
        rep = run(history, i, pref, selections)
        sys.stdout.flush()
        px.append(i)
        for k in xrange(3):
            py[k].append(rep[k])
    plt.axhline(y=0.0, color='k', alpha=0.2)
    print json.dumps(selections)
    for k in xrange(3):
        mean = np.array(py[k]).mean()
        notes += 'pos %d, mean = %.24f\n' % (k, mean)
        print 'pos %d, mean = %.24f' % (k, mean)
        plt.plot(px, py[k], pc[k])
        plt.axhline(y=mean, color=pc[k][:-1], alpha=0.3)
    sys.stdout.flush()
    plt.figtext(0.14, 0.11, notes, alpha=0.3, horizontalalignment='left', fontsize=6, multialignment='left', fontweight='normal')
    #plt.show()
    plt.savefig(img)

if __name__ == '__main__':
    main()
