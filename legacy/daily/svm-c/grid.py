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
from widget import autoscale

# config
key = [1, 2, 3, 4, 5, 6, 7, 8, 9]
nlabels = 10
nsample = 30
ntracks = 30
enscale = False


def run(tday=0):
    timer = timer_c()
    matT = numpy.empty((0, len(key)*ntracks), dtype='f')
    resT = numpy.array([], dtype='i')
    boundary = None
    if enscale:
        numpy.zeros((len(key), 2), dtype='f')
        for i in xrange(len(boundary)):
            boundary[i][0]=numpy.inf
            boundary[i][1]=-numpy.inf
    with open('../data/dbf/2017.dbf', 'r') as dbf:
        history = json.load(dbf)
        print 'run tday = %s' % (history['record'].values()[0][tday][0])
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
            if len(table)<tday+181:
                continue
            # skip the stock has suspended in 90 trading days
            if table[89][0]!=first:
                continue
            # form mat & res
            for i in xrange(tday+1, tday+1+nsample):
                # mat++
                row = []
                for r in xrange(i+1, i+ntracks+1):
                    for offset in key:
                        row.append(table[r][offset])
                matT = numpy.append(matT, numpy.array([row], dtype='f'), axis=0)
                # res++
                hg = table[i][seven] + 10.0
                hg = min(hg, 19.99)
                hg = max(hg, 0.0)
                resT = numpy.append(resT, int(hg/(20.0/nlabels)))
            # boundray-update
            if enscale:
                for i in xrange(nsample+ntracks+1):
                    for j in xrange(len(key)):
                        boundary[j][0] = min(boundary[j][0], table[i][key[j]])
                        boundary[j][1] = max(boundary[j][1], table[i][key[j]])
    if enscale:
        autoscale(matT, boundary)
    print 'matT & resT loaded successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    #
    timer.reset()
    matQ = numpy.empty((0, len(key)*ntracks), dtype='f')
    resQ = numpy.array([], dtype='i')
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
            # mat++
            row = []
            for r in xrange(tday+1, tday+1+ntracks):
                for offset in key:
                    row.append(table[r][offset])
            matQ = numpy.append(matQ, numpy.array([row], dtype='f'), axis=0)
            # res++
            hg = table[tday][seven] + 10.0
            hg = min(hg, 19.99)
            hg = max(hg, 0.0)
            resQ = numpy.append(resQ, int(hg/(20.0/nlabels)))
    if enscale:
        autoscale(matQ, boundary)
    print 'matQ & resQ loaded successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    sys.stdout.flush()
    for i in xrange(-6, 6, 2):
        for j in xrange(-6, 6, 2):
            cost = 10.**i
            gamma = 10.**j
            param = '-s 0 -t 2 -c %f -g %f -b 0 -q' % (cost, gamma)
            print 'param = %s' % param
            #
            timer.reset()
            lsvm = svmutil.svm_train(resT.tolist(), matT.tolist(), param)
            print 'svm trained successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
            timer.reset()
            p_labels, p_acc, p_vals = svmutil.svm_predict(resT.tolist(), matT.tolist(), lsvm, '')
            print 'svm predicted successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
            timer.reset()
            p_labels, p_acc, p_vals = svmutil.svm_predict(resQ.tolist(), matQ.tolist(), lsvm, '')
            print 'svm predicted successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
            print [ [ int(x) for x in p_labels ].count(i) for i in xrange(nlabels)]
            sys.stdout.flush()

def main():
    run()

if __name__ == '__main__':
    main()
