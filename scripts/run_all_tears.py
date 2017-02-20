#!/usr/bin/env python2

from __future__ import print_function

import os
import sys
import time
import math

if len(sys.argv) != 8:
    print("usage: {} <kfdist> <chunksize> <quality_start> <quality_end> <quality_step> <region> <nworkers>".format(sys.argv[0]))
    sys.exit(1)

def runcommand(command):
    print(command)
    return os.system(command)

TOTAL_CHUNKS = 2936
RUN_K = "REGION={region} FRAMES={num_frames} ~/excamera-results/scripts/run_K_tears.sh {kfdist} {nworkers} {offset} {quality}"

kfdist = int(sys.argv[1])
num_frames = int(sys.argv[2])
start = int(sys.argv[3])
end = int(sys.argv[4])
step = int(sys.argv[5])
nworkers = int(sys.argv[7])

if num_frames == 12:
    TOTAL_CHUNKS /= 2
elif num_frames == 24:
    TOTAL_CHUNKS /= 4

NUM_WORKERS = [min(nworkers, TOTAL_CHUNKS - i * nworkers) for i in range(int(math.ceil(1.0 * TOTAL_CHUNKS / nworkers)))]

with open("run_log_%s" % time.time(), "w") as runlog:
    for quality_level in range(start, end + 1, step):
        for i in range(len(NUM_WORKERS)):
            try_count = 0

            while True:
                time.sleep(10)
                try_count += 1
                retval = runcommand(RUN_K.format(region=sys.argv[6],
                                                 kfdist=kfdist,
                                                 num_frames=num_frames,
                                                 nworkers=NUM_WORKERS[i],
                                                 offset=sum(NUM_WORKERS[:i]),
                                                 quality=quality_level))

                if retval != 0:
                    if try_count >= 5:
                        runlog.write("Failed: {} -> {}\n".format(quality_level, i))
                        runlog.flush()
                        break

                else:
                    runlog.write("Succeed: {} -> {}\n".format(quality_level, i))
                    runlog.flush()
                    break

        runlog.write("\n")
