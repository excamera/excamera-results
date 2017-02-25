#!/bin/bash

for k in 01 #02 04 08 16
do
  for s in 24 #06 12 24
  do
    cd k${k}_s${s}

    SINTEL_TOTAL_CHUNKS=3552
    TEARS_TOTAL_CHUNKS=2936

    if [ "${s}" -eq "24" ]
    then
      SINTEL_TOTAL_CHUNKS=1776
      TEARS_TOTAL_CHUNKS=1468
    fi


    if [ -d "sintel" ]
    then
      cd sintel

      printf "" >../../results/sintel-s${s}_k${k}.dat

      for i in $(ls)
      do
        cd ${i}
        echo "Processing sintel-s${s}_k${k}-${i}..."
        echo "# ${i}" >>../../../results/sintel-s${s}_k${k}.dat
        ~/projects/excamera-results/scripts/xc-plotter ${s} ${SINTEL_TOTAL_CHUNKS} >>../../../results/sintel-s${s}_k${k}.dat
        cd ..
      done
      cd ..
    fi

    if [ -d "tears" ]
    then
      cd tears

      printf "" >../../results/tears-s${s}_k${k}.dat

      for i in $(ls)
      do
        cd ${i}
        echo "Processing tears-s${s}_k${k}-${i}..."
        echo "# ${i}" >>../../../results/tears-s${s}_k${k}.dat
        ~/projects/excamera-results/scripts/xc-plotter ${s} ${TEARS_TOTAL_CHUNKS} >>../../../results/tears-s${s}_k${k}.dat
        cd ..
      done
      cd ..
    fi

    cd .. 
  done
done
