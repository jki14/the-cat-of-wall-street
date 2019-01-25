# -*- coding: utf-8 -*-

import json
import numpy
import sys
import time

def main():
    foo = None

    with open('data/dbf/2016.dbf', 'r') as dbf:
        foo = json.load(dbf)

    dates = []
    for code, table in foo['record'].iteritems():
        if len(table)>=360:
            if len(dates)>0:
                err = False
                for i in xrange(360):
                    if table[i][0] != dates[i]:
                        err = True
                if err:
                    print '%s bad dates' % (code)
            else:
                for i in xrange(360):
                    dates.append(table[i][0])
    for i in xrange(len(dates)):
        print dates[i]

if __name__ == '__main__':
    main()
