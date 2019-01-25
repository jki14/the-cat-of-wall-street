# -*- coding: utf-8 -*-

import json
import numpy
import sys
import time

def main():
    foo = None

    with open('data/dbf/2017.dbf', 'r') as dbf:
        foo = json.load(dbf)

    dates = []
    for table in foo['record'].values():
        for row in table:
            if row[0] not in dates:
                dates.append(row[0])
    dates.sort(reverse=True)
    for row in dates:
        print row

if __name__ == '__main__':
    main()
