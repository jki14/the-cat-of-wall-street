#! /bin/bash

python expect.py 0 51 ss 2017.png >2017.log 2>&1 &
python expect.py 51 101 ss 2016.png >2016.log 2>&1 &
python expect.py 101 153 ss 2015.png >2015.log 2>&1 &
python expect.py 153 206 ss 2014.png >2014.log 2>&1 &
python expect.py 206 258 ss 2013.png >2013.log 2>&1 &
