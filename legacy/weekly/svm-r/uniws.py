# -*- coding: utf-8 -*-

import json
import numpy
import os
import sys
import time

if '../public' not in sys.path:
    sys.path.append('../public')
from widget import history_c

def main():
    history = history_c()
    #history.load('../../daily/163/data/dbf/2016.dbf')
    #history.load('../../daily/163/data/dbf/2012.dbf')
    history.load('../../daily/163/data/dbf/overview.dbf')
    foo = history.uniws()
    for row in foo[::-1]:
        print row

if __name__ == '__main__':
    main()
