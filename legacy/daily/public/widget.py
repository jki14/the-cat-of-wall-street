# -*- coding: utf-8 -*-

import json
import time
import matplotlib.pyplot as plt

class timer_c:
    __stamp = 0.0
    def __init__(self):
        self.__stamp = time.time()
    def reset(self):
        self.__stamp = time.time()
    def lag(self):
        return time.time()-self.__stamp

class history_c:
    __foo = None
    def load(self, path):
        self.__foo = {}
        self.__foo['dates'] = []
        self.__foo['daily'] = {}
        with open(path, 'r') as dbf:
            src = json.load(dbf)
            key = src['layout'].index('PCHG')
            for code, table in src['record'].iteritems():
                self.__foo['daily'][code] = {}
                self.__foo['daily'][code]['features'] = []
                self.__foo['daily'][code]['dates'] = []
                prev = '2038-01-19'
                for row in table:
                    if None in row:
                        continue
                    if row[0] >= prev:
                        raise ValueError
                    prev = row[0]
                    if row[0] not in self.__foo['dates']:
                        self.__foo['dates'].append(row[0])
                    self.__foo['daily'][code]['features'].append(row[key:key+1] + row[1:key] + row[key+1:])
                    self.__foo['daily'][code]['dates'].append(row[0])
        self.__foo['dates'].sort(reverse=True)
    def grab(self, nsample, ntracks, doffset=-1, freclen=90, fnonsup=30):
        fnonsup = max(fnonsup, ntracks)
        freclen = max(freclen, fnonsup)
        w = []
        x = []
        y = []
        for code, detail in self.__foo['daily'].iteritems():
            for dayid in xrange(doffset, doffset+nsample):
                # get rowid & check X valid
                rowid = 0
                datex = self.__foo['dates'][dayid+1]
                datef = self.__foo['dates'][dayid+fnonsup]
                try:
                    rowid = detail['dates'].index(datex)
                except ValueError:
                    continue
                if len(detail['dates'])<rowid+freclen:
                    continue
                if detail['dates'][rowid+fnonsup-1]!=datef:
                    continue
                # append y'
                if dayid == -1:
                    y.append(0.0)
                else:
                    datey = self.__foo['dates'][dayid]
                    if rowid>0 and detail['dates'][rowid-1]==datey:
                        y.append(detail['features'][rowid-1][0])
                    else:
                        continue
                # append x'
                row = []
                for i in xrange(rowid, rowid+ntracks):
                    row = row + detail['features'][i]
                x.append(row)
                # append w'
                w.append(code)
        return w, x, y

def plotdraw(x, y, title='figure', path=None):
    plt.axvline(x=0.0, color='k', alpha=0.2)
    plt.axhline(y=0.0, color='k', alpha=0.2)
    plt.plot(x, y, '.')
    if path is None:
        plt.show()
