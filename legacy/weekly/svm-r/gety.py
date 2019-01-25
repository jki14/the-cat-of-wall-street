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

def run(history, tweek):
    w, x, y = history.grab(1, 1, tweek, '', -1, -1, -1)
    x = xfilter(x)
    while True:
        try:
            code = raw_input().strip()
            try:
                offset = w.index(code)
            except ValueError:
                print 'invalid code'
                continue
            print '%s: %.6f' % (w[offset], y[offset])
        except KeyboardInterrupt:
            break

def main():
    tweek = -1
    try:
        tweek = int(sys.argv[1])
    except IndexError, ValueError:
        print 'error: tweek was not found.'
        return
    history = history_c()
    history.load('../../daily/163/data/dbf/2016.dbf')
    print 'history loaded successfully'
    run(history, tweek)

if __name__ == '__main__':
    main()
