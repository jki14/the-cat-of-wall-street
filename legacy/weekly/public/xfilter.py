def xfilter(x):
    f = []
    for row in x:
        g = [ row[i*12+j] for i in xrange(len(row)/12) for j in xrange(12) if j not in [5, 10, 11] ]
        for i in xrange(len(g)/9):
            g[i*9+7] /= 100.0
            g[i*9+8] /= 10000.0
            #g[i*9+8] /= g[i*9+7]*1.0
            #g[i*9+7] /= 10.0**6
        f.append(g)
    return f
