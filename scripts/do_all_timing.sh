#!/bin/bash -e

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <root-folder> <result-folder>"
    exit 1
fi

sintel[06-0]="xcenc_transitions_k*_n880_o0_*"
sintel[06-1]="xcenc_transitions_k*_n896_o880_*"
sintel[06-2]="xcenc_transitions_k*_n880_o1776_*"
sintel[06-3]="xcenc_transitions_k*_n896_o2656_*"

sintel[12-0]="xcenc_transitions_k*_n880_o0_*"
sintel[12-1]="xcenc_transitions_k*_n896_o880_*"

sintel[24-0]="xcenc_transitions_k*_n888_o0_*"

tears[06-0]="xcenc_transitions_k*_n736_o0_*"
tears[06-1]="xcenc_transitions_k*_n736_o736_*"
tears[06-2]="xcenc_transitions_k*_n736_o1472_*"
tears[06-3]="xcenc_transitions_k*_n728_o2208_*"

tears[12-0]="xcenc_transitions_k*_n736_o0_*"
tears[12-1]="xcenc_transitions_k*_n732_o736_*"

tears[24-0]="xcenc_transitions_k*_n734_o0_*"

ROOT_FOLDER=$1
RES_FOLDER=$2

mkdir -p ${RES_FOLDER}
mkdir -p ${RES_FOLDER}/final

for k in 01 02 04 08 16
do
  for s in 06 12 24
  do
    if [ "$s" -gt "12" ] && [ "$k" -gt "04" ]; then
      # We didn't process (12, 8) and (12, 16).
      continue
    fi

    for movie in sintel tears
    do
      echo "Processing ${movie}-s${s}_k${k}..."

      FOLDER=${ROOT_FOLDER}/${movie}-s${s}_k${k}-logs

      if [ -d "${FOLDER}" ]
      then
        if [ "${s}" -eq "06" ]
        then
          for i in 0 1 2 3
          do
            LOGFILE=$movie[${s}-${i}]
            ./xc-time.py region ${FOLDER}/${!LOGFILE} > ${RES_FOLDER}/${movie}-s${s}_k${k}-${i}.stats
          done
        elif [ "${s}" -eq "12" ]
        then
          for i in 0 1
          do
            LOGFILE=$movie[${s}-${i}]
            ./xc-time.py region ${FOLDER}/${!LOGFILE} > ${RES_FOLDER}/${movie}-s${s}_k${k}-${i}.stats
          done
        else
          for i in 0
          do
            LOGFILE=$movie[${s}-${i}]
            ./xc-time.py region ${FOLDER}/${!LOGFILE} > ${RES_FOLDER}/${movie}-s${s}_k${k}-${i}.stats
          done
        fi

        ./xc-time.py total ${RES_FOLDER}/${movie}-s${s}_k${k}-*.stats >${RES_FOLDER}/final/${movie}-s${s}_k${k}-total.stats
      fi
    done
  done
done
