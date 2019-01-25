# -*- coding: utf-8 -*-

import csv
import datetime
import json
import os
import socket
import sys
import time
import urllib2

tracking_list = ['sh000001', 'sz399001', 'sz399300']

foo = {}

try:
    with open('./data/dbf/overview.dbf', 'r') as dbf:
        foo = json.load(dbf)
except IOError:
    foo['layout'] = ['DATE', 'TCLOSE','HIGH','LOW','TOPEN','LCLOSE','CHG','PCHG','TURNOVER','VOTURNOVER','VATURNOVER','TCAP','MCAP']
    foo['record'] = {}

x = 0
y = len(tracking_list)

for code in tracking_list:
    first = '19910101'
    if code not in foo['record']:
        foo['record'][code] = []
    elif len(foo['record'][code])>0:
        tmp = time.strptime(foo['record'][code][0][0], '%Y-%m-%d')
        nxt = datetime.date(tmp.tm_year, tmp.tm_mon, tmp.tm_mday) + datetime.timedelta(1)
        first = nxt.strftime('%Y%m%d')
    code163 = code.replace('sh', '0').replace('sz', '1')
    url = 'http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=20380119&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP' % (code163, first)
    rep = None
    raw = None
    sup = 0.0
    while True:
        try:
            rep = urllib2.urlopen(url, timeout=1)
            raw = list(csv.reader(rep))
        except (urllib2.URLError, socket.error, socket.timeout) as e:
            sup += 0.2
            time.sleep(sup)
            continue
        break
    bunk = []
    for row in raw[1:]:
        contents = [row[0]]
        for i in xrange(3, 15):
            cell = row[i]
            if cell != '':
                if cell != 'None':
                    cell = float(cell)
                else:
                    cell = None
            else:
                cell = 0.0
            contents.append(cell)
        bunk.append(contents)
    foo['record'][code] = bunk + foo['record'][code]
    x += 1
    print '%d/%d + %d' % (x, y, len(bunk))
    sys.stdout.flush()
    #time.sleep(0.2)

with open('./data/dbf/overview.dbf', 'w') as dbf:
    json.dump(foo, dbf)
    print 'dbf have been written successfully'
    sys.stdout.flush()
