# -*- coding: utf-8 -*-

import json
import numpy
import os
import sys
import time

if '../public' not in sys.path:
    sys.path.append('../public')
from widget import history_c
from xfilter import xfilter

import matplotlib.pyplot as plt

def regression(history, sample, strategy):
    tot = 0.0
    for row in sample:
        tot += history.keypoint3(row[0], row[1], strategy)
    return tot

def progress(history, sample):
    foo = []
    for x in xrange(-10, 10):
        for y in xrange(1, 21):
            for z in xrange(1, 21):
                pro = (1.0+x*0.01, 1.0+y*0.01, 1.0-z*0.01)
                foo.append((regression(history, sample, pro), pro))
    foo.sort(key = lambda tup: (tup[0]))
    for row in foo:
        print row

def main():
    history = history_c()
    history.load('../../daily/163/data/dbf/2012.dbf')
    jstr = raw_input().strip()
    task = json.loads(jstr)
    n = len(task['code'])
    sample = [(task['code'][i], task['tweek'][i]) for i in xrange(n)]
    progress(history, sample)

if __name__ == '__main__':
    main()
