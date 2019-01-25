# -*- coding: utf-8 -*-

import json
import numpy
import sys
import time

def main():
    
    lhs, rhs = None, None
    with open('../data/dbf/2017.dbf', 'r') as dbf:
        lhs = json.load(dbf)
    with open('../data/dbf/2017.dbf', 'r') as dbf:
        rhs = json.load(dbf)

    # base on lhs
    for code, table in lhs['record'].iteritems():
        if code in rhs.keys():
            lht = table
            rht = rhs['record'][code]
            if len(lht) == len(rht):
                for r in xrange(len(lht)):
                    if len(lht[r]) == len(rht[r]):
                        diff = False
                        for c in xrange(len(lht[r])):
                            if lht[r][c] != rht[r][c]:
                                diff = True
                        if diff:
                            print 'lhs[\'record\'][%s][%d]:\n%s\nrhs[\'record\'][%s][%d]:\n%s' % (code, r, str(lht[r]), code, r, str(rht[r]))
                    else:
                        print 'lhs[\'record\'][%s][%d] contains %d elements, rhs[\'record\'][%s][%d] contains %d elements' % (code, len(lht), len(lht[r]), code, len(rht), len(rht[r]))
            else:
                print 'lhs[\'record\'][%s] contains %d lines, rhs[\'record\'][%s] contains %d lines' % (code, len(lht), code, len(rht))
        else:
            print '%s found in lhs but not in rhs' % (code)
    for code in rhs['record'].keys():
        if code not in lhs['record'].keys():
            print '%s found in rhs but not in lhs' % (code)

if __name__ == '__main__':
    main()
