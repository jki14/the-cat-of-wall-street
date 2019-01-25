# -*- coding: utf-8 -*-

import json
import numpy
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

# config
key = [1, 2, 3, 4, 5, 6, 7, 8, 9]
nlabels = 10
nsample = 3
ntracks = 30

def main():
    timer = timer_c()
    res = numpy.array([], dtype='i')
    mat = numpy.empty((0, len(key)*ntracks), dtype='f')
    with open('../data/dbf/2017.dbf', 'r') as dbf:
        history = json.load(dbf)
        seven = history['layout'].index('PCHG')
        print 'seven at %d.' % (seven)
        first = None
        for code, table in history['record'].iteritems():
            if len(table)<180:
                continue
            if first is None or first<table[89][0]:
                first = table[89][0]
        for code, table in history['record'].iteritems():
            # skip the stock has less than 180 rows of record
            if len(table)<180:
                continue
            # skip the stock has suspended in 90 trading days
            if table[89][0]!=first:
                continue
            # form mat & res
            for i in xrange(nsample):
                # mat++
                row = []
                for r in xrange(i+1, i+ntracks+1):
                    for offset in key:
                        row.append(table[r][offset])
                mat = numpy.append(mat, numpy.array([row], dtype='f'), axis=0)
                # res++
                hg = table[i][seven] + 10.0
                hg = min(hg, 19.99)
                hg = max(hg, 0.0)
                res = numpy.append(res, int(hg/(20.0/nlabels)))
    print 'mat & res loaded successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    #
    timer.reset()
    lsvm = svmutil.svm_train(res.tolist(), mat.tolist(), '-s 0 -t 0 -g 1.00 -c 1000000.00 -b 0 -q')
    svmutil.svm_save_model('temp.svm', lsvm)
    print 'svm trained successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    p_labels, p_acc, p_vals = svmutil.svm_predict(res.tolist(), mat.tolist(), lsvm, '')

if __name__ == '__main__':
    main()
