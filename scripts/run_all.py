#!/usr/bin/env python2

from __future__ import print_function

import os
import sys
import time

if len(sys.argv) != 6:
    print("usage: run_all.py <kfdist> <chunksize> <start> <end> <region>")
    sys.exit(1)

def runcommand(command):
    print(command)
    return os.system(command)

TOTAL_CHUNKS = 3552

RUN_K = "REGION={region} ~/excamera-results/scripts/run_K.sh {kfdist} {nworkers} {offset} {quality}"

start = int(sys.argv[3])
end = int(sys.argv[4])

NUM_WORKERS = [min(888, TOTAL_CHUNKS - i * 888) for i in range(4)]

with open("run_log_%s" % time.time(), "w") as runlog:
    for quality_level in range(start, end, 2):
        for i in range(4):
            try_count = 0

            while True:
                time.sleep(10)
                try_count += 1
                retval = runcommand(RUN_K.format(region=sys.argv[5], 
                                                 kfdist=sys.argv[1],
                                                 nworkers=NUM_WORKERS[i],
                                                 offset=sum(NUM_WORKERS[:i]),
                                                 quality=quality_level))

                if retval != 0:
                    if try_count >= 5:
                        runlog.write("Failed: {} -> {}\n".format(quality_level, i))
                        break

                else:
                    runlog.write("Succeed: {} -> {}\n".format(quality_level, i))
                    break

        runlog.write("\n")
