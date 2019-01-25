with open('2017.dbf', 'r') as dbf:
    raw = dbf.read()
    print raw.count('2017-09-21')
