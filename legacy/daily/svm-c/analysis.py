import csv

with open('benchmark.csv', 'r') as log:
    tab = list(csv.reader(log))
    col = len(tab[0])
    a = [ [ [ [0, 0] for i in xrange(col)  ] for j in xrange(col) ] for k in xrange(len(tab)/col) ]
    f = [ [ [ [0, 0] for i in xrange(col)  ] for j in xrange(col) ] for k in xrange(len(tab)/col) ]
    pix = [ [ [0, 0] for i in xrange(col)  ] for j in xrange(col) ]
    for r in xrange(len(tab)):
        for c in xrange(col):
            if tab[r][c]!='nil':
                value, count = tab[r][c].split(' ')
                value = float(value)
                count = int(count[1:-1])
                a[r/col][r%col][c] = [value, count]
                f[r/col][r%col][c] = [value, count]
                pix[r%col][c][0] += value
                pix[r%col][c][1] += 1
    print 'pix:'
    for r in xrange(col):
        row = ''
        for c in xrange(col):
            if c>0:
                row += ', '
            if pix[r][c][1]>0:
                row += '%.6f (%d)' % (pix[r][c][0], pix[r][c][1])
            else:
                row += 'nil'
        print row
    print 'rag:'
    for d in xrange(len(f)):
        for r in reversed(xrange(col)):
            for c in reversed(xrange(col)):
                f[d][r][c][0] *= f[d][r][c][1]
                if r+1<col:
                    f[d][r][c][0] += f[d][r+1][c][0] * f[d][r+1][c][1]
                    f[d][r][c][1] += f[d][r+1][c][1]
                if c+1<col:
                    f[d][r][c][0] += f[d][r][c+1][0] * f[d][r][c+1][1]
                    f[d][r][c][1] += f[d][r][c+1][1]
                if r+1<col and c+1<col:
                    f[d][r][c][0] -= f[d][r+1][c+1][0] * f[d][r+1][c+1][1]
                    f[d][r][c][1] -= f[d][r+1][c+1][1]
                if f[d][r][c][1]>0:
                    f[d][r][c][0] /= f[d][r][c][1]
    rag = [ [ [0, 0] for i in xrange(col)  ] for j in xrange(col) ]
    for d in xrange(len(f)):
        for r in xrange(col):
            for c in xrange(col):
                if f[d][r][c][1]>0:
                    rag[r][c][0] += f[d][r][c][0]
                    rag[r][c][1] += 1
    for r in xrange(col):
        row = ''
        for c in xrange(col):
            if c>0:
                row += ', '
            if rag[r][c][1]>0:
                row += '%.6f (%d)' % (rag[r][c][0], rag[r][c][1])
            else:
                row += 'nil'
        print row
