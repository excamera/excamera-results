#!/usr/bin/env python2

from __future__ import print_function

import os
import sys
import time

if len(sys.argv) != 6:
    print("usage: {} <movie=sintel|tears> <region> <chunk-size> <region-index> <repeat-count>".format(sys.argv[0]))
    sys.exit(1)

def runcommand(command):
    print(command)
    time.sleep(10)
    return os.system(command)

y_values = {
    6: (
        (1, 32),
        (2, 22),
        (4, 16),
        (8, 12),
        (16, 12),
    ),
    12: (
        (1, 26),
        (2, 16),
        (4, 12),
        (8, 11),
        (16, 11),
    )
}

movie = sys.argv[1]
region = sys.argv[2]
num_frames = int(sys.argv[3])
idx = int(sys.argv[4])
REPEAT_TIMES = int(sys.argv[5])

assert(movie == "sintel" or movie == "tears")
assert((num_frames == 6 and idx <= 3) or (num_frames == 12 and idx <= 1))

if movie == "sintel":
    TOTAL_CHUNKS = 3552

    if num_frames == 6:
        NUM_WORKERS = [880, 896, 880, 896]
    elif num_frames == 12:
        NUM_WORKERS = [880, 896]
else:
    TOTAL_CHUNKS = 2936

    if num_frames == 6:
        NUM_WORKERS = [736, 736, 736, 728]
    elif num_frames == 12:
        NUM_WORKERS = [736, 732]

RUN_K = "NOUPLOAD=1 REGION={region} FRAMES={num_frames} ~/excamera-results/scripts/run_K{movie}.sh {kfdist} {nworkers} {offset} {quality}"

with open("run_log_%s" % time.time(), "w") as runlog:
    for K, y in y_values[num_frames]:
        for i in range(REPEAT_TIMES):
            print("Speed test ({}) for s{:02d}_k{:02d}".format(i, num_frames, K))

            retval = runcommand(RUN_K.format(region=region,
                                             kfdist=K,
                                             num_frames=num_frames,
                                             nworkers=NUM_WORKERS[idx],
                                             offset=sum(NUM_WORKERS[:idx]),
                                             quality=y,
                                             movie='_tears' if movie == 'tears' else ''))

            if retval == 0:
                print("[OK] speed test ({}) for s{:02d}_k{:02d}".format(i, num_frames, K), file=runlog)
            else:
                print("[FAIL] speed test ({}) for s{:02d}_k{:02d}".format(i, num_frames, K), file=runlog)
