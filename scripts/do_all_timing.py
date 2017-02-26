#!/usr/bin/env python2

from __future__ import division, print_function

import os
import sys

from speed_run import y_values

if len(sys.argv) != 3:
    print("usage: {} <root-folder> <result-folder>".format(sys.argv[0]))
    sys.exit(1)


name_patterns = {
    'sintel' : {
        6: {
            0: "xcenc_transitions_k*_n880_o0_*",
            1: "xcenc_transitions_k*_n896_o880_*",
            2: "xcenc_transitions_k*_n880_o1776_*",
            3: "xcenc_transitions_k*_n896_o2656_*",
        },
        12: {
            0: "xcenc_transitions_k*_n880_o0_*",
            1: "xcenc_transitions_k*_n896_o880_*",
        },
        24: {
            0: "xcenc_transitions_k*_n888_o0_*",
        }
    },
    'tears': {
        6: {
            0: "xcenc_transitions_k*_n736_o0_*",
            1: "xcenc_transitions_k*_n736_o736_*",
            2: "xcenc_transitions_k*_n736_o1472_*",
            3: "xcenc_transitions_k*_n728_o2208_*",
        },
        12: {
            0: "xcenc_transitions_k*_n736_o0_*",
            1: "xcenc_transitions_k*_n732_o736_*",
        },
        24: {
            0: "xcenc_transitions_k*_n734_o0_*",
        }
    }
}

ROOT_FOLDER = sys.argv[1]
RESULT_FOLDER = sys.argv[2]

for k in [1, 2, 4, 8, 16]:
    for s in [6, 12, 24]:
        if s > 12 and k > 4: continue

        for movie in ["sintel", "tears"]:
            ys = filter(lambda x: x[0] == k, y_values[movie][s])[0][1]

            for y in ys:
                for i in range(24 // s):
                    os.system("./xc-time.py region {root_folder}/{movie}-s{s:02d}_k{k:02d}-logs/{pattern}y{y}* >{res_folder}/{movie}-s{s:02d}_k{k:02d}-y{y:02d}-{i}.stats"
                              .format(pattern=name_patterns[movie][s][i],
                                      y=y,
                                      root_folder=ROOT_FOLDER,
                                      res_folder=RESULT_FOLDER,
                                      movie=movie, s=s, k=k, i=i))

                os.system("./xc-time.py total {res_folder}/{movie}-s{s:02d}_k{k:02d}-y{y:02d}-*.stats >{res_folder}/final/{movie}-s{s:02d}_k{k:02d}-y{y:02d}-total.stats"
                          .format(pattern=name_patterns[movie][s][i],
                                  y=y,
                                  res_folder=RESULT_FOLDER,
                                  movie=movie, s=s, k=k))
