#!/usr/bin/env python3
import sys

line_count = 0

for line in sys.stdin:
    line = line.strip()
    if line_count % 4 == 1:   # Line 2 of every FASTQ read
        for i, base in enumerate(line):
            if base in ["A", "T", "G", "C"]:
                print(f"{i}\t{base}")
    line_count += 1