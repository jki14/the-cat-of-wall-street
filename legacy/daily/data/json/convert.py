# -*- coding: utf-8 -*-

import json

raw = ''
while True:
    try:
        raw += raw_input()
    except EOFError:
        break

foo = json.loads(raw)

print json.dumps(foo, encoding='ascii')
