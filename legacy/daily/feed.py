# -*- coding: utf-8 -*-

import csv
import datetime
import json
import os
import socket
import time
import urllib2

tracking_list = []
with open('./data/json/sh-list-a.json', 'r') as list_file:
    tracking_list += json.load(list_file)
#with open('./data/json/sh-list-b.json', 'r') as list_file:
    #tracking_list += json.load(list_file)
#with open('./data/json/sz-list-a.json', 'r') as list_file:
    #tracking_list += json.load(list_file)
#with open('./data/json/sz-list-b.json', 'r') as list_file:
    #tracking_list += json.load(list_file)

foo = {}

try:
    with open('./data/dbf/2016.dbf', 'r') as dbf:
        foo = json.load(dbf)
except IOError:
    foo['layout'] = ['DATE', 'TOPEN', 'TCLOSE', 'CHG', 'PCHG', 'LOW', 'HIGH', 'VOTURNOVER','VATURNOVER', 'TURNOVER']
    foo['record'] = {}

x = 0
y = len(tracking_list)
z = []

for code in tracking_list:
    first = '20160101'
    if code not in foo['record']:
        foo['record'][code] = []
    elif len(foo['record'][code])>0:
        tmp = time.strptime(foo['record'][code][0][0], '%Y-%m-%d')
        nxt = datetime.date(tmp.tm_year, tmp.tm_mon, tmp.tm_mday) + datetime.timedelta(1)
        first = nxt.strftime('%Y%m%d')
    code163 = code.replace('sh', '0').replace('sz', '1')
    url = 'http://q.stock.sohu.com/hisHq?code=cn_%s&start=%s&end=20380119&stat=0&order=D&period=d&rt=jsonp' % (code163[1:], first)
    rep = None
    while True:
        try:
            rep = urllib2.urlopen(url)
        except urllib2.URLError, socket.error:
            time.sleep(0.2)
            continue
        break
    raw = json.loads(rep.read().strip()[9:-1])
    if len(raw)==0:
        z.append((code, url))
        continue
    bunk = []
    for row in raw[0]['hq']:
        contents = [row[0]]
        for i in xrange(1, 10):
            cell = row[i]
            cell = cell.replace('%', '')
            try:
                cell = float(cell)
            except ValueError:
                if cell == '-':
                    cell = 0.0
                else:
                    print '%s\n%s\n' % (url, row[0])
                    raise IOError
            contents.append(cell)
        bunk.append(contents)
    foo['record'][code] = bunk + foo['record'][code]
    x += 1
    print '%d/%d + %d' % (x, y, len(bunk))
    #time.sleep(0.2)

for row in z:
    print '%s => %s' % row

with open('./data/dbf/2016.dbf', 'w') as dbf:
    json.dump(foo, dbf)
    print 'dbf have been written successfully'
