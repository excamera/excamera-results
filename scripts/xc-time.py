#!/usr/bin/env python3

import os
import sys
import json
import statistics
import pdb

def read_log_file(path):
    stats = {'total_time': 0}

    with open(path) as fin:
        for line in fin:
            line = line.strip()

            if len(line) == 0:
                continue

            line = line.split(":", 1)[1]
            data = eval(line)

            assert(data[-1][1] == "FinalState")

            final_time = data[-1][0]

            stats['total_time'] = max(stats['total_time'], final_time)

    return stats

def process_repetitive_runs(log_files):
    all_runs = []

    for log_file in log_files:
        all_runs += [read_log_file(log_file)['total_time']]

    return {
        'min': min(all_runs),
        'max': max(all_runs),
        'avg': statistics.mean(all_runs),
        'median': statistics.median(all_runs),
        #'stdev': statistics.stdev(all_runs)
    }

def process_whole_run(stat_files):
    all_stats = []

    for stat_file in stat_files:
        with open(stat_file) as fin:
            all_stats += [json.load(fin)['median']]

    return (
        ('min', min(all_stats)),
        ('max', max(all_stats)),
        ('avg', statistics.mean(all_stats)),
        ('median', statistics.median(all_stats)),
        #('stdev', statistics.stdev(all_stats)),
    )


command = sys.argv[1]

if command == "region":
    print(json.dumps(process_repetitive_runs(sys.argv[2:])))
elif command == "total":
    data = process_whole_run(sys.argv[2:])
    print("# " + " ".join([str(x[0]) for x in data]))
    print(" ".join([str(x[1]) for x in data]))
