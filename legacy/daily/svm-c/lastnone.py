# -*- coding: utf-8 -*-

import json
import numpy
import sys
import time

def main():
    with open('../data/dbf/2017.dbf', 'r') as dbf:
        history = json.load(dbf)
        for code, table in history['record'].iteritems():
            if None in table[0]:
                print code

if __name__ == '__main__':
    main()
