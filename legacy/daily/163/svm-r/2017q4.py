# -*- coding: utf-8 -*-

import sys

# nsample = 5
# ntracks = 5
# options = '-s 3 -t 2 -g %.12f -c %.12f -b 0 -q' % (2.0**-24, 2.0**24)

def main():
    foo = []
    goo = [(11.710860291975045,2.4606),(42.369737361871884,1.2322),(24.545282858596856,0.2173),(45.79796270962124,1.1139),(42.89625580036777,1.3932),(42.70796608201151,0.1422),(21.092721014218707,-0.1292),(19.57634890257044,0.4785),(19.835832466293084,3.8043),(9.230345062196864,0.6617),(8.474274823793053,0.4386),(7.944459748103107,0.7796),(6.928828049433188,0.7178),(22.614094834604444,0.3119),(13.187038428273066,2.7229),(14.589735952795166,0.8104),(20.842974958005453,-0.0416),(19.7769158778542,-0.3398),(23.222686002958458,-8.2627),(20.02650021483962,-2.4171),(13.180083196481458,0.0826),(9.960201063915024,-2.9382),(8.589610970872675,-3.951),(6.018559106517212,1.3363),(5.138933331121271,-2.1095),(4.714298923001919,0.8902),(5.394613495218829,0.3355),(2.8041302696993196,0.1421),(5.809987873382523,-0.2646),(7.024394253062882,-0.2534),(4.61137248876887,-6.5095),(5.674111609101278,0.0),(5.584247804598519,-1.4154),(5.489665099021007,-0.3394),(5.8089075050864105,2.6478),(5.415989482733719,3.3997),(5.767377811922786,-0.9143),(4.315452797794193,0.558),(5.022527668155789,0.0707),(2.6862829886954955,-0.9057),(3.9689267897708236,0.0),(6.189063154033268,0.336),(7.041786098566509,1.8131),(6.523336131308805,0.6641),(7.594720506435826,-1.685),(10.29913896848929,-1.9057),(7.062712589888213,-0.1233),(8.212922483963903,4.1059),(4.579178623187247,-0.789),(4.324996448265889,1.472),(4.893283158719955,0.1116),(7.096961112023696,0.4983),(4.560163028954729,-0.8179),(4.253036849319791,-1.25),(6.210583844149076,-0.464),(4.871194554995549,0.1714),(3.6397749944398377,1.4092),(3.5459380589120157,-0.5014),(3.5205021364780076,1.3521),(4.932817726403049,-0.539)]
    lower_bound = float(sys.argv[1])
    for row in goo:
        if row[0]>lower_bound-1e-6:
            foo.append(row[1])
    print '%.9f(%d)' % (sum(foo)/len(foo), len(foo))

if __name__=='__main__':
    main()
