#!/bin/bash

for k in 02 04 08 16
do
  for s in 06 12
  do
    cd k${k}_s${s}

    if [ -d "sintel" ]
    then
      cd sintel
      for i in $(ls)
      do
        cd ${i}
        echo "# ${i}" >>../../../results/sintel-s${s}_k${k}.dat
        ~/projects/excamera-paper-graphs/xc-plotter ${s} 3552 >>../../../results/sintel-s${s}_k${k}.dat
        cd ..
      done
      cd ..
    fi

    if [ -d "tears" ]
    then
      cd tears
      for i in $(ls)
      do
        cd ${i}
        echo "# ${i}" >>../../../results/tears-s${s}_k${k}.dat
        ~/projects/excamera-paper-graphs/xc-plotter ${s} 2936 >>../../../results/tears-s${s}_k${k}.dat
        cd ..
      done
      cd ..
    fi

    cd .. 
  done
done
