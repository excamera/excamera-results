#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage ${0} <ssims-folder> <out-folder>"
  exit 1
fi

SSIMS_DIR=$1
OUT_DIR=$2

declare -A TOTAL_CHUNKS
TOTAL_CHUNKS["sintel_06"]=3552
TOTAL_CHUNKS["tears_06"]=2936
TOTAL_CHUNKS["sintel_12"]=3552
TOTAL_CHUNKS["tears_12"]=2936
TOTAL_CHUNKS["sintel_24"]=1776
TOTAL_CHUNKS["tears_24"]=1468

for s in 06 12 24
do
  for k in 01 02 04 08 16
  do
    if [ "$s" -gt "12" ] && [ "$k" -gt "04" ]; then
      # We didn't process (12, 8) and (12, 16).
      continue
    fi

    for movie in sintel tears
    do
      THIS_SSIM_DIR=${SSIMS_DIR}/s${s}_k${k}/${movie}
      OUT_FILE=${OUT_DIR}/${movie}-s${s}_k${k}.dat

      if [ ! -d "${THIS_SSIM_DIR}" ]; then
        echo "${THIS_SSIM_DIR} doesn't exist."
        continue
      fi

      echo -n "" >${OUT_FILE}
      for i in $(ls ${THIS_SSIM_DIR})
      do
        CHUNK_COUNT=TOTAL_CHUNKS["${movie}_${s}"]

        echo "Processing ${movie}-s${s}_k${k}@${i}..."

        echo "# ${i}" >>${OUT_FILE}
        ~/projects/excamera-results/scripts/xc-plotter ${THIS_SSIM_DIR}/${i} ${s} ${!CHUNK_COUNT} >>${OUT_FILE}
      done
    done
  done
done
