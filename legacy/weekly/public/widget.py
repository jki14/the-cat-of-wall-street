# -*- coding: utf-8 -*-

import json
import sys
import time

from datetime import datetime

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
        self.__foo['dates'] = set()
        self.__foo['weeks'] = []
        self.__foo['uniws'] = []
        self.__foo['daily'] = {}
        self.__foo['title'] = []
        with open(path, 'r') as dbf:
            src = json.load(dbf)
            key = src['layout'].index('PCHG')
            vot = src['layout'].index('VOTURNOVER')
            self.__foo['title'] = src['layout'][key:key+1] + src['layout'][1:key] + src['layout'][key+1:]
            for code, table in src['record'].iteritems():
                code = code.encode('ascii');
                self.__foo['daily'][code] = {}
                self.__foo['daily'][code]['features'] = []
                self.__foo['daily'][code]['dates'] = []
                self.__foo['daily'][code]['turnover'] = []
                prev = '2038-01-19'
                pres = 0
                for row in table:
                    if None in row:
                        continue
                    if row[0] >= prev:
                        raise ValueError
                    prev = row[0]
                    #if row[0] not in self.__foo['dates']:
                        #self.__foo['dates'].append(row[0])
                    self.__foo['dates'].add(row[0])
                    self.__foo['daily'][code]['features'].append(row[key:key+1] + row[1:key] + row[key+1:])
                    pres += row[vot]
                    self.__foo['daily'][code]['turnover'].append(pres)
                    self.__foo['daily'][code]['dates'].append(row[0])
                self.__foo['daily'][code]['turnover'].append(0)
        self.__foo['dates'] = list(self.__foo['dates'])
        self.__foo['dates'].sort(reverse=True)
        for dt in self.__foo['dates']:
            self.__foo['weeks'].append(int(str(int(dt[:4])) + datetime.strptime(dt, '%Y-%m-%d').strftime('%W')))
        last = ''
        for ws in self.__foo['weeks']:
            if ws != last:
                self.__foo['uniws'].append(ws)
                last = ws
    def grab(self, nsample, ntracks, woffset=-1, pref='', freclen=180, fnonsup=90, active=-1):
        topen = self.__foo['title'].index('TOPEN')
        tclose = self.__foo['title'].index('TCLOSE')
        fnonsup = max(fnonsup, ntracks)
        freclen = max(freclen, fnonsup)
        w = []
        x = []
        y = []
        for code, detail in self.__foo['daily'].iteritems():
            if len(pref)>0 and not code.startswith(pref):
                continue
            for weekid in xrange(woffset, woffset+nsample):
                # get rowid & check X valid
                ws = self.__foo['uniws'][weekid+1]
                dayid = self.__foo['weeks'].index(ws) - 1
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
                if detail['turnover'][rowid+ntracks-1] - detail['turnover'][rowid-1] < active * ntracks * 100:
                    continue
                # append y'
                if weekid == -1:
                    y.append(0.0)
                else:
                    ws = self.__foo['uniws'][weekid]
                    sunday = self.__foo['weeks'].index(ws)
                    monday = sunday
                    sunid = 0
                    monid = 0
                    while self.__foo['weeks'][monday+1] == ws:
                        monday += 1
                    try:
                        sunid = detail['dates'].index(self.__foo['dates'][sunday])
                        monid = detail['dates'].index(self.__foo['dates'][monday])
                    except ValueError:
                        continue
                    if sunid-monid == sunday-monday:
                        value = (detail['features'][sunid][tclose]-detail['features'][monid][topen])*1.0/detail['features'][monid][topen]
                        #value = (detail['features'][sunid][topen]-detail['features'][monid][topen])*1.0/detail['features'][monid][topen]
                        y.append(value*100.0)
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
    def uniws(self):
        foo = []
        revws = self.__foo['weeks'][::-1]
        revdt = self.__foo['dates'][::-1]
        index = 0
        for ws in self.__foo['uniws']:
            cnt = 0
            head = revws.index(ws)
            for i in xrange(head, len(revdt)):
                if revws[i] == ws:
                    cnt += 1
                else:
                    break
            foo.append('%3d:%s:%s:(%d)' % (index, ws, revdt[head], cnt))
            index += 1
        return foo
    def kweek(self, code, weekid):
        topen = self.__foo['title'].index('TOPEN')
        tclose = self.__foo['title'].index('TCLOSE')
        higp = self.__foo['title'].index('HIGH')
        lowp = self.__foo['title'].index('LOW')
        try:
            detail = self.__foo['daily'][code]
            ws = self.__foo['uniws'][weekid+1]
            dayid = self.__foo['weeks'].index(ws) - 1
            rowid = 0
            datex = self.__foo['dates'][dayid+1]
            try:
                rowid = detail['dates'].index(datex)
            except ValueError:
                return (0.0, 0.0, 0.0, 0)
            ws = self.__foo['uniws'][weekid]
            sunday = self.__foo['weeks'].index(ws)
            monday = sunday
            sunid = 0
            monid = 0
            while self.__foo['weeks'][monday+1] == ws:
                monday += 1
            try:
                sunid = detail['dates'].index(self.__foo['dates'][sunday])
                monid = detail['dates'].index(self.__foo['dates'][monday])
            except ValueError:
                return (0.0, 0.0, 0.0, 0)
            if sunid-monid == sunday-monday:
                value = (detail['features'][sunid][tclose]-detail['features'][monid][topen])*1.0/detail['features'][monid][topen]
                higv = detail['features'][monid][higp]
                lowv = detail['features'][monid][lowp]
                for i in xrange(sunid, monid):
                    higv = max(higv, detail['features'][i][higp])
                    lowv = min(lowv, detail['features'][i][lowp])
                higv = (higv-detail['features'][monid][topen])*1.0/detail['features'][monid][topen]
                lowv = (lowv-detail['features'][monid][topen])*1.0/detail['features'][monid][topen]
                return (value*100.0, higv*100.0, lowv*100.0, monid-sunid+1)
            else:
                return (0.0, 0.0, 0.0, 0)
        except KeyError:
            return (0.0, 0.0, 0.0, 0)
    def keypoint3(self, code, weekid, strategy):
        topen = self.__foo['title'].index('TOPEN')
        tclose = self.__foo['title'].index('TCLOSE')
        higp = self.__foo['title'].index('HIGH')
        lowp = self.__foo['title'].index('LOW')
        try:
            detail = self.__foo['daily'][code]
            ws = self.__foo['uniws'][weekid+1]
            dayid = self.__foo['weeks'].index(ws) - 1
            rowid = 0
            datex = self.__foo['dates'][dayid+1]
            try:
                rowid = detail['dates'].index(datex)
            except ValueError:
                return 0.0
            ws = self.__foo['uniws'][weekid]
            sunday = self.__foo['weeks'].index(ws)
            monday = sunday
            sunid = 0
            monid = 0
            while self.__foo['weeks'][monday+1] == ws:
                monday += 1
            try:
                sunid = detail['dates'].index(self.__foo['dates'][sunday])
                monid = detail['dates'].index(self.__foo['dates'][monday])
            except ValueError:
                return 0.0
            if sunid-monid == sunday-monday:
                buy = detail['features'][monid][topen] * strategy[0]
                gain = buy * strategy[1]
                loss = buy * strategy[2]
                for i in xrange(monid, sunid-1, -1):
                    if detail['features'][i][lowp]<buy:
                        while i>=sunid:
                            if detail['features'][i][lowp]<loss:
                                return (loss - buy) * 100.0 / buy
                            if detail['features'][i][higp]>gain:
                                return (gain - buy) * 100.0 / buy
                            i -= 1
                        return (detail['features'][sunid][tclose] - buy) * 100.0 / buy
                        break
                return 0.0
            else:
                return 0.0
        except KeyError:
            return 0.0

def plotdraw(x, y, title='figure', path=None):
    if 'pyplot' not in sys.modules:
        import matplotlib.pyplot as plt
    plt.axvline(x=0.0, color='k', alpha=0.2)
    plt.axhline(y=0.0, color='k', alpha=0.2)
    plt.plot(x, y, '.')
    if path is None:
        plt.show()
