# -*- coding: utf-8 -*-

import json
import numpy
import sys
import time

def main():
    foo = None

    with open('../data/dbf/2017.dbf', 'r') as dbf:
        foo = json.load(dbf)

    last = '1990-01-01'
    for code, table in foo['record'].iteritems():
        if table[0][0]>last:
            last = table[0][0]
    print 'last = %s' % (last)
    for code, table in foo['record'].iteritems():
        if table[0][0]<last:
            print '%s expired on %s' % (code, table[0][0])

if __name__ == '__main__':
    main()
