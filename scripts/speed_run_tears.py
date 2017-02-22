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
        (1, 30),
        (2, 24),
        (4, 20),
        (8, 18),
        (16, 16),
    ) ),
    (12, (
        (1, 27),
        (2, 20),
        (4, 18),
        (8, 16),
        (16, 16),
    ) )
)

region = sys.argv[1]
idx = int(sys.argv[2])
REPEAT_TIMES = int(sys.argv[3])

if idx > 3:
    print("invalid region-index.")
    sys.exit(1)

TOTAL_CHUNKS = 2936
RUN_K = "NOUPLOAD=1 REGION={region} FRAMES={num_frames} ~/excamera-results/scripts/run_K_tears.sh {kfdist} {nworkers} {offset} {quality}"

NUM_WORKERS = [736, 736, 736, 728]

with open("run_log_%s" % time.time(), "w") as runlog:
    for S, v in y_values:
        for K, y in v:
            done_file = "/tmp/tears_s{:02d}_k{:02d}_{}.done".format(S, K, idx)
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
