# -*- coding: utf-8 -*-

import json
import numpy
import sys
import time

def main():
    foo = None

    with open('../data/dbf/2017.dbf', 'r') as dbf:
        foo = json.load(dbf)

    for code, table in foo['record'].iteritems():
        for i in xrange(len(table)):
            if None in table[i]:
                print '%s @ %s' % (code, table[i][0])

if __name__ == '__main__':
    main()
