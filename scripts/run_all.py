#!/usr/bin/env python2

from __future__ import print_function

import os
import sys
import time
import math

if len(sys.argv) != 9:
    print("usage: run_all.py <movie=sintel|tears> <kfdist> <chunksize> <quality_start> <quality_end> <quality_step> <region> <nworkers>")
    sys.exit(1)

def runcommand(command):
    print(command)
    time.sleep(10)
    return os.system(command)

movie = sys.argv[1]
kfdist = int(sys.argv[2])
num_frames = int(sys.argv[3])
start = int(sys.argv[4])
end = int(sys.argv[5])
step = int(sys.argv[6])
region = sys.argv[7]
nworkers = int(sys.argv[8])

assert(movie == "sintel" or movie == "tears")

if movie == "sintel":
    TOTAL_CHUNKS = 3552
elif movie == "tears":
    TOTAL_CHUNKS = 2936

if num_frames == 12:
    TOTAL_CHUNKS /= 2
elif num_frames == 24:
    TOTAL_CHUNKS /= 4

NUM_WORKERS = [min(nworkers, TOTAL_CHUNKS - i * nworkers) for i in range(int(math.ceil(1.0 * TOTAL_CHUNKS / nworkers)))]

RUN_K = "REGION={region} FRAMES={num_frames} ~/excamera-results/scripts/run_K.sh {movie} {kfdist} {nworkers} {offset} {quality}"

with open("run_log_%s" % time.time(), "w") as runlog:
    for quality_level in range(start, end + 1, step):
        for i in range(len(NUM_WORKERS)):
            try_count = 0

            while True:
                try_count += 1
                retval = runcommand(RUN_K.format(region=region,
                                                 kfdist=kfdist,
                                                 num_frames=num_frames,
                                                 nworkers=NUM_WORKERS[i],
                                                 offset=sum(NUM_WORKERS[:i]),
                                                 quality=quality_level,
                                                 movie=movie))

                if retval != 0:
                    if try_count >= 5:
                        runlog.write("Failed: {}: {} -> {}\n".format(movie, quality_level, i))
                        runlog.flush()
                        break

                else:
                    runlog.write("Succeed: {}: {} -> {}\n".format(movie, quality_level, i))
                    runlog.flush()
                    break

        runlog.write("\n")
