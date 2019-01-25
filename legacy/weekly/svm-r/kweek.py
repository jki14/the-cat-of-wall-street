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

def main():
    history = history_c()
    history.load('../../daily/163/data/dbf/2012.dbf')
    plt.axhline(y=0.0, color='k', alpha=0.2)
    jstr = raw_input().strip()
    task = json.loads(jstr)
    n = len(task['code'])
    for i in xrange(n):
        row = history.kweek(task['code'][i], task['tweek'][i])
        co = 'r'
        if row[0]<1e-6:
            co = 'g'
        li = '-'
        if row[3]<5:
            li = '--'
        plt.plot([i, i], [row[1], row[2]], co+li)
        plt.plot([i], [row[1]], co+',')
        plt.plot([i], [row[2]], co+',')
        plt.plot([i], [row[0]], co+'o')
    #plt.plot([-1, n], [0, 0], '.', alpha=1.0)
    plt.xlim(-1, n)
    plt.show()

if __name__ == '__main__':
    main()
