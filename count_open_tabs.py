import json
import time

def _sum_change(ls):
    count = 0
    for l in ls:
        if l[0] == '-':
            count -= 1
        elif l[0] == '+':
            count += 1
    return count

def _line_sets(lines):
    """Break lines into sets of lines (entries in the log file)"""
    start = 0
    while start < len(lines):
        stop = start+1
        while stop < len(lines) and lines[stop][0] != "=":
            stop += 1
        yield lines[start:stop]
        start = stop

def run(log_file, output_file):
    with open(log_file, 'r') as f:
        log_lines = f.readlines()

    data = []
    prev_count = 0
    for ls in _line_sets(log_lines):
        new_count = prev_count + _sum_change(ls[1:])
        data.append([int(ls[0][1:]), new_count])
        prev_count = new_count

    with open(output_file, 'w') as f:
        json.dump(data, f, separators=(',', ':'))  # separators to make it compact
