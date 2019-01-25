import sys

with open('benchmark.log', 'r') as log:
    for line in log:
        if ',' in line and 'key' not in line:
             sys.stdout.write(line)
