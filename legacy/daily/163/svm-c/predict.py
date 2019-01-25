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

if '../../public' not in sys.path:
    sys.path.append('../../public')
from widget import timer_c

# config
key = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]
nlabels = 10
nsample = 3
ntracks = 30

def main():
    timer = timer_c()
    tag = []
    res = numpy.array([], dtype='i')
    mat = numpy.empty((0, len(key)*ntracks), dtype='f')
    with open('../data/dbf/2016.dbf', 'r') as dbf:
        history = json.load(dbf)
        seven = history['layout'].index('PCHG')
        first = None
        for code, table in history['record'].iteritems():
            # skip the stock has less than 180 rows of record
            if len(table)<180:
                continue
            # skip the stock has suspended in 90 trading days
            if len([i for i in xrange(90) if None in table[i]])>0:
                continue
            # mat++
            row = []
            for r in xrange(ntracks):
                for offset in key:
                    row.append(table[r][offset])
            mat = numpy.append(mat, numpy.array([row], dtype='f'), axis=0)
            # res++
            hg = table[0][seven] + 10.0
            hg = min(hg, 19.99)
            hg = max(hg, 0.0)
            res = numpy.append(res, int(hg/(20.0/nlabels)))
            # tag++
            tag.append(code)
    print 'mat & res loaded successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    #
    timer.reset()
    lsvm = svmutil.svm_load_model('temp.svm')
    labels = lsvm.get_labels()
    nlabel = len(labels)
    p_labels, p_acc, p_vals = svmutil.svm_predict(res.tolist(), mat.tolist(), lsvm, '')
    print 'svm predicted successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    best = []
    for idx in xrange(len(tag)):
        votes = numpy.zeros(nlabel, dtype='i')
        k = 0
        for i in xrange(nlabel):
            for j in xrange(i+1, nlabel):
                if p_vals[idx][k] > 0.0:
                    votes[i] += 1
                else:
                    votes[j] += 1
                k += 1
        bar = []
        for i in xrange(nlabel):
            bar.append((labels[i], votes[i]))
        bar = sorted(bar, key = lambda tup: (-tup[1], tup[0]))
        #if tag[idx]=='sh600326':
        #    print '%d, %d, %d \n' % (bar[0][0], bar[1][0], bar[2][0])
        if int(p_labels[idx]) in [bar[0][0], bar[1][0]]:
            if int(p_labels[idx])==bar[1][0]:
                bar[0], bar[1] = bar[1], bar[0]
        else:
            continue
        #print bar
        if bar[0][0]>=nlabels-2:
            best.append((tag[idx], bar[0][0], bar[1][0], bar[2][0]))
    best = sorted(best, key = lambda tup: (-tup[1], -tup[2], -tup[3], tup[0]))
    for row in best:
        print '%s => %d %d %d' % row

if __name__ == '__main__':
    main()
