# -*- coding: utf-8 -*-

import json
import numpy as np
import sys
import time

def main():
    foo = None

    with open('data/dbf/2017.dbf', 'r') as dbf:
        foo = json.load(dbf)

    goo = []
    pos = foo['layout'].index('VOTURNOVER')
    for table in foo['record'].values():
        for row in table:
            goo.append(row[pos])
    goo = np.array(goo)
    print 'low = %.2f' % goo.min()
    print 'hig = %.2f' % goo.max()
    print 'mean = %.2f' % goo.mean()

if __name__ == '__main__':
    main()
