# -*- coding: utf-8 -*-

import json
import sys
import time

from datetime import datetime

class overview_c:
    __foo = None
    def __init__(self, path):
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

    def earlierThan(self, dates, key):
        lef = 0
        rig = len(dates)-1
        while lef<=rig:
            mid = (lef+rig)>>1
            if dates[mid]<key:
                if mid==lef or dates[mid-1]>=key:
                    return mid
                rig = mid-1
            else:
                lef = mid+1
        raise ValueError

    def notLater(self, dates, key):
        lef = 0
        rig = len(dates)-1
        while lef<=rig:
            mid = (lef+rig)>>1
            if dates[mid]<=key:
                if mid==lef or dates[mid-1]>key:
                    return mid
                rig = mid-1
            else:
                lef = mid+1
        raise ValueError


    def deltaPrint(self, handIn, handOut):
        tclose = self.__foo['title'].index('TCLOSE')
        for code, detail in self.__foo['daily'].iteritems():
            x = self.earlierThan(detail['dates'], handIn)
            y = self.notLater(detail['dates'], handOut)
            x = detail['features'][x][tclose]
            y = detail['features'][y][tclose]
            print '%s %s->%s %.6f (%.6f <- %.6f)' % (code, handIn, handOut, (y-x)*100.0/x, y, x)
            sys.stdout.flush()

def main():
    overview = overview_c('../../daily/163/data/dbf/overview.dbf')
    while True:
        try:
            handIn, handOut = raw_input().strip().split()
            overview.deltaPrint(handIn, handOut)
        except ValueError:
            continue
        except EOFError:
            break

if __name__ == '__main__':
    main()
