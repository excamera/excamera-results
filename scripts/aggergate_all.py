#!/usr/bin/env python2

from __future__ import division, print_function

import os
import sys
import numpy as np

from speed_run import y_values

# s     => chunk size
# k     => keyframe distance
# movie => sintel | tears

if len(sys.argv) != 4:
    print("usage: {} <result-folder> <timing-folder> <output-folder>".format(sys.argv[0]))
    sys.exit(1)

RESULT_FOLDER = sys.argv[1]
TIMING_FOLDER = sys.argv[2]
OUTPUT_FOLDER = sys.argv[3]

def generate_data_point(movie, s, k):
    print("Processing {}-s{:02d}_k{:02d}".format(movie, s, k))

    k_file_num = k

    if k == 1 and s != 24:
        if movie == "sintel":
            k_file_num = 16 if s == 6 else 8
        else:
            k_file_num = 16 if s == 6 else 2

    result_file = "{movie}-s{s:02d}_k{k:02d}.dat".format(movie=movie, s=s, k=k_file_num)
    result_file = os.path.join(RESULT_FOLDER, result_file)
    target_ys = filter(lambda x: x[0] == k, y_values[movie][s])[0][1]

    with open(result_file) as fin:
        result_data = [x.strip() for x in fin.readlines()]

    ys_data = []

    for target_y in target_ys:
        data = []
        for i in range(len(result_data)):
            if result_data[i].strip() == "# y{:02d}".format(target_y):
                if k == 1:
                    data += [float(x) for x in result_data[i+2].split(" ")[1::-1]]
                else:
                    data += [float(x) for x in result_data[i+2].split(" ")[:1:-1]]

        if not data:
            print(result_file)
            print(target_y)
            raise Exception("Could not find SSIM vs Bitrate data for this.")

        timing_file = "{movie}-s{s:02d}_k{k:02d}-y{y:02d}-total.stats".format(movie=movie, s=s, k=k, y=target_y)
        timing_file = os.path.join(TIMING_FOLDER, timing_file)

        with open(timing_file) as fin:
            timing_data = [x.strip() for x in fin.readlines()]

        if len(timing_data) < 2 or not timing_data[0].startswith("# "):
            raise Exception("Invalid timing data.")

        timing_data = dict(zip(timing_data[0][2:].strip().split(" "), timing_data[1].strip().split(" ")))
        data += [float(timing_data["max"].strip())]

        ys_data += [data]

    if len(ys_data) == 1:
        return ys_data[0]

    inv = np.linalg.inv(np.array([[ys_data[0][0], ys_data[1][0]],
                                  [1,             1]
                                 ]))

    if movie == "sintel":
        AB = np.dot(inv , np.array([[20], [1]]))
    elif movie == "tears":
        AB = np.dot(inv , np.array([[16], [1]]))
        
    new_s = np.dot(np.array([[ys_data[0][0], ys_data[1][0]]]), AB)[0,0]
    new_b = np.dot(np.array([[ys_data[0][1], ys_data[1][1]]]), AB)[0,0]
    new_t = np.dot(np.array([[ys_data[0][2], ys_data[1][2]]]), AB)[0,0]

    return [new_s, new_b, new_t, movie, s, k]

for movie in ["sintel", "tears"]:
    for s in [6, 12, 24]:
        output_file = "{movie}-s{s:02d}.points".format(movie=movie, s=s)
        output_file = os.path.join(OUTPUT_FOLDER, output_file)

        with open(output_file, "w") as fout:
            for k in [1, 2, 4, 8, 16]:
                if s == 24 and k > 4: continue

                d = generate_data_point(movie=movie, s=s, k=k)
                #fout.write("# bitrate (Mbits/s), mean SSIM (dB), {} time (s), movie, s, k, y\n".format(TARGET_MEASURE))
                fout.write("{}\n".format("\t".join([str(x) for x in d])))
