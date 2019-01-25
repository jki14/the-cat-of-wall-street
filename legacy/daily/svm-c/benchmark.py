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
nsample = 3
ntracks = 30
enscale = False


def run(tday, logfile):
    logstr = ''
    timer = timer_c()
    res = numpy.array([], dtype='i')
    rat = numpy.array([], dtype='f')
    mat = numpy.empty((0, len(key)*ntracks), dtype='f')
    boundary = None
    if enscale:
        numpy.zeros((len(key), 2), dtype='f')
        for i in xrange(len(boundary)):
            boundary[i][0]=numpy.inf
            boundary[i][1]=-numpy.inf
    with open('../data/dbf/2017.dbf', 'r') as dbf:
        history = json.load(dbf)
        date = '1990-01-01'
        date2 = '1990-01-01'
        for table in history['record'].values():
            if len(table)<180:
                continue
            if date < table[tday][0]:
                date = table[tday][0]
            if date2 < table[tday+1][0]:
                date2 = table[tday+1][0]
        print 'run tday = %s' % (date)
        logstr += 'tday = %s\n' % (date)
        seven = history['layout'].index('PCHG')
        print 'seven at %d.' % (seven)
        first = '1990-01-01'
        for code, table in history['record'].iteritems():
            offset2 = -1
            for i in xrange(len(table)):
                if table[i][0] < date2:
                    break
                elif table[i][0] == date2:
                    offset2 = i
                    break
            if offset2<0:
                continue
            if len(table)<offset2+180:
                continue
            if first<table[offset2+89][0]:
                first = table[offset2+89][0]
        for code, table in history['record'].iteritems():
            offset2 = -1
            for i in xrange(len(table)):
                if table[i][0] < date2:
                    break
                elif table[i][0] == date2:
                    offset2 = i
                    break
            if offset2<0:
                continue
            # skip the stock has less than 180 rows of record
            if len(table)<offset2+180:
                continue
            # skip the stock has suspended in 90 trading days
            if table[offset2+89][0]!=first:
                continue
            # form mat & res
            for i in xrange(offset2, offset2+nsample):
                # mat++
                row = []
                for r in xrange(i+1, i+ntracks+1):
                    for pos in key:
                        row.append(table[r][pos])
                mat = numpy.append(mat, numpy.array([row], dtype='f'), axis=0)
                # res++
                hg = table[i][seven] + 10.0
                hg = min(hg, 19.99)
                hg = max(hg, 0.0)
                res = numpy.append(res, int(hg/(20.0/nlabels)))
                rat = numpy.append(rat, table[i][seven])
            # boundray-update
            if enscale:
                for i in xrange(nsample+ntracks+1):
                    for j in xrange(len(key)):
                        boundary[j][0] = min(boundary[j][0], table[i][key[j]])
                        boundary[j][1] = max(boundary[j][1], table[i][key[j]])
    if enscale:
        autoscale(mat, boundary)
    print 'mat & res loaded successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    #
    timer.reset()
    lsvm = svmutil.svm_train(res.tolist(), mat.tolist(), '-s 0 -t 0 -g 1.00 -c 1000000.00 -b 0 -q')
    #svmutil.svm_save_model('benchmark.svm', lsvm)
    #lsvm = svmutil.svm_load_model('benchmark.svm')
    print 'svm trained successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    p_labels, p_acc, p_vals = svmutil.svm_predict(res.tolist(), mat.tolist(), lsvm, '')
    #
    timer.reset()
    tag = []
    res = numpy.array([], dtype='i')
    rat = numpy.array([], dtype='f')
    mat = numpy.empty((0, len(key)*ntracks), dtype='f')
    with open('../data/dbf/2017.dbf', 'r') as dbf:
        history = json.load(dbf)
        seven = history['layout'].index('PCHG')
        print 'seven at %d.' % (seven)
        first = '1990-01-01'
        for code, table in history['record'].iteritems():
            offset = -1
            for i in xrange(len(table)):
                if table[i][0] < date:
                    break
                elif table[i][0] == date:
                    offset = i
                    break
            if offset<0:
                continue
            if len(table)<offset+181:
                continue
            if first<table[offset+90][0]:
                first = table[offset+90][0]
        for code, table in history['record'].iteritems():
            offset = -1
            for i in xrange(len(table)):
                if table[i][0] < date:
                    break
                elif table[i][0] == date:
                    offset = i
                    break
            if offset<0:
                continue
            # skip the stock has less than 180 rows of record
            if len(table)<offset+181:
                continue
            # skip the stock has suspended in 90 trading days
            if table[offset+90][0]!=first:
                continue
            # mat++
            row = []
            for r in xrange(offset+1, offset+1+ntracks):
                for pos in key:
                    row.append(table[r][pos])
            mat = numpy.append(mat, numpy.array([row], dtype='f'), axis=0)
            # res++
            hg = table[offset][seven] + 10.0
            hg = min(hg, 19.99)
            hg = max(hg, 0.0)
            res = numpy.append(res, int(hg/(20.0/nlabels)))
            rat = numpy.append(rat, table[offset][seven])
            # tag++
            tag.append(code)
    if enscale:
        autoscale(mat, boundary)
    print 'mat & res loaded successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    #
    timer.reset()
    labels = lsvm.get_labels()
    nlabel = len(labels)
    p_labels, p_acc, p_vals = svmutil.svm_predict(res.tolist(), mat.tolist(), lsvm, '')
    print 'svm predicted successfully in %s sec.' % (str(float('{0:.3f}'.format(timer.lag()))))
    summary = numpy.zeros((nlabels, 2), dtype='i')
    details = numpy.zeros((nlabels, nlabels), dtype='i')
    #goals = numpy.zeros((nlabels, nlabels), dtype='i')
    profit2 = [ [ [] for i in xrange(nlabels) ] for j in xrange(nlabels) ]
    #for idx in xrange(len(tag)):
    #    votes = numpy.zeros(nlabel, dtype='i')
    #    k = 0
    #    for i in xrange(nlabel):
    #        for j in xrange(i+1, nlabel):
    #            if p_vals[idx][k] > 0.0:
    #                votes[i] += 1
    #            else:
    #                votes[j] += 1
    #            k += 1
    #    bar = []
    #    for i in xrange(nlabel):
    #        bar.append((labels[i], votes[i]))
    #    bar = sorted(bar, key = lambda tup: (-tup[1], tup[0]))
    #    if bar[0][0] == res[idx]:
    #        summary[res[idx]][0] += 1
    #    summary[res[idx]][1] += 1
    #print summary
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
        if p_labels[idx] == res[idx]:
            summary[res[idx]][0] += 1
        summary[res[idx]][1] += 1
        details[int(p_labels[idx])][res[idx]] += 1
	if int(p_labels[idx]) in (bar[0][0], bar[1][0]):
            profit2[int(p_labels[idx])][bar[0][0]^bar[1][0]^int(p_labels[idx])].append(rat[idx])
        #if tag[idx]=='sh600326':
        #    print '%d %d %d => %.6f' % (bar[0][0], bar[1][0], bar[2][0], rat[idx])
        #details[min(bar[0][0], bar[1][0])][res[idx]] += 1
        #if p_labels[idx]>=nlabels-1:
        #if max(bar[0][0], bar[1][0])>=9:
            #goals[min(bar[0][0], bar[1][0])][res[idx]] += 1
    print summary
    print details
    for i in xrange(nlabels):
        foo = ''
        for j in xrange(nlabels):
            if j>0:
                foo += ', '
                logstr += ','
            if len(profit2[i][j])>0:
                foo += '%.6f (%d)' % (sum(profit2[i][j])/len(profit2[i][j]), len(profit2[i][j]))
                logstr += '%.6f (%d)' % (sum(profit2[i][j])/len(profit2[i][j]), len(profit2[i][j]))
            else:
                foo += 'nil'
                logstr += 'nil'
        print foo
        logstr += '\n'
    #print goals
    logstr += '\n'
    with open(logfile, 'a') as log:
        log.write(logstr)

def main():
    print 'key = %s' % (str(key).replace(',', ''))
    print 'nlabels = %d' % (nlabels)
    print 'nsample = %d' % (nsample) 
    print 'ntracks = %d' % (ntracks)
    print 'enscale = %s' % (str(enscale))
    argv = sys.argv
    argc = len(argv)
    lef, rig, logfile = 0, 1, 'benchmark.log'
    if argc>3:
        lef = int(argv[1])
        rig = int(argv[2])
        logfile = argv[3]
    with open(logfile, 'a') as log:
        log.write('key = %s\nnlabels = %d\nnsample = %d\nntracks = %d\nenscale = %s\n\n' % (str(key), nlabels, nsample, ntracks, str(enscale)))
    for i in xrange(lef, rig):
        run(i, logfile)
        sys.stdout.flush()

if __name__ == '__main__':
    main()
