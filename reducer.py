#!/usr/bin/env python3
import sys
from collections import defaultdict

counts = defaultdict(lambda: {'A':0, 'T':0, 'G':0, 'C':0})

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    pos, base = line.split('\t')
    counts[int(pos)][base] += 1

for pos in sorted(counts.keys()):
    print(pos, counts[pos]['A'], counts[pos]['T'], counts[pos]['G'], counts[pos]['C'])