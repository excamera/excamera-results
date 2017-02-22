#!/usr/bin/env python2

from __future__ import print_function

import os
import sys
import time

if len(sys.argv) != 4:
    print("usage: {} <region> <region-index> <repeat-count>".format(sys.argv[0]))
    sys.exit(1)

def runcommand(command):
    print(command)
    time.sleep(10)
    return os.system(command)

y_values = (
    (6, (
        (1, 32),
        (2, 22),
        (4, 16),
        (8, 12),
        (16, 12),
    ) ),
    (12, (
        (1, 26),
        (2, 16),
        (4, 12),
        (8, 11),
        (16, 11),
    ) )
)

region = sys.argv[1]
idx = int(sys.argv[2])
REPEAT_TIMES = int(sys.argv[3])

if idx > 3:
    print("invalid region-index.")
    sys.exit(1)

TOTAL_CHUNKS = 3552
RUN_K = "NOUPLOAD=1 REGION={region} FRAMES={num_frames} ~/excamera-results/scripts/run_K.sh {kfdist} {nworkers} {offset} {quality}"

NUM_WORKERS = [880, 896, 880, 896]

with open("run_log_%s" % time.time(), "w") as runlog:
    for S, v in y_values:
        for K, y in v:
            done_file = "/tmp/sintel_s{:02d}_k{:02d}_{}.done".format(S, K, idx)
            if os.path.exists(done_file):
                continue

            for i in range(REPEAT_TIMES):
                print("Speed test ({}) for s{:02d}_k{:02d}".format(i, S, K))

                retval = runcommand(RUN_K.format(region=region,
                                                 kfdist=K,
                                                 num_frames=S,
                                                 nworkers=NUM_WORKERS[idx],
                                                 offset=sum(NUM_WORKERS[:idx]),
                                                 quality=y))

                if retval == 0:
                    print("[OK] speed test ({}) for s{:02d}_k{:02d}".format(i, S, K), file=runlog)
                else:
                    print("[FAIL] speed test ({}) for s{:02d}_k{:02d}".format(i, S, K), file=runlog)

            os.system("touch {}".format(done_file))
