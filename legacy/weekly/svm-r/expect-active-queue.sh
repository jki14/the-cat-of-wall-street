#! /bin/bash

python expect-active.py 0 51 sh a2017-sh.png >a2017-sh.log 2>&1
python expect-active.py 51 101 sh a2016-sh.png >a2016-sh.log 2>&1
python expect-active.py 101 153 sh a2015-sh.png >a2015-sh.log 2>&1
python expect-active.py 153 206 sh a2014-sh.png >a2014-sh.log 2>&1
python expect-active.py 206 258 sh a2013-sh.png >a2013-sh.log 2>&1
