#!/bin/bash

set -e

. ~/excamera-results/scripts/env_setup

FN_NAME[6]=xc-enc_3cGUvto2
FN_NAME[12]=xc-enc_3cGUvto2
FN_NAME[24]=xc-enc_24frames

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ] || [ -z "$5" ]; then
    echo "Usage: $0 movie kf_dist n_workers n_offset y_val"
    exit 1
fi

MOVIE=$1; shift

PUBLIC_IP=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)
MU_ROOT=/home/excamera/git/github.com/mu/src/lambdaize/

KFDIST=$1
NWORKERS=$2
NOFFSET=$3
YVAL=$4
if [ -z "$PORTNUM" ]; then
    PORTNUM=13579
fi
if [ -z "$STATEPORT" ]; then
    STATEPORT=13330
fi
if [ -z "$STATETHREADS" ]; then
    STATETHREADS=24
fi
if [ ! -z "$DEBUG" ]; then
    DEBUG="-D"
else
    DEBUG=""
fi
if [ ! -z "$NOUPLOAD" ]; then
    echo "WARNING: no upload"
    UPLOAD=""
else
    UPLOAD="-u"
fi
if [ -z "$SSIM_ONLY" ]; then
    SSIM_ONLY=""
else
    SSIM_ONLY=1
fi
if [ -z "$FRAMES" ]; then
    NUM_FRAMES=6
else
    NUM_FRAMES=$FRAMES
fi
FRAME_STR=$(printf "_%02d" $NUM_FRAMES)
if [ -z "$SEVEN_FRAMES" ]; then
    VID_SUFFIX=$FRAME_STR
    XCENC_EXEC="xcenc"
    if [ "$NUM_FRAMES" -eq "6" ]; then
        DUMP_EXEC="dump_ssim"
    elif [ "$NUM_FRAMES" -eq "12" ]; then
        DUMP_EXEC="split12_dump_ssim"
    else
        DUMP_EXEC="split_dump_ssim"
    fi
    FRAME_SWITCH=""
else
    VID_SUFFIX=""
    XCENC_EXEC="xcenc7"
    DUMP_EXEC="dump_ssim7"
    FRAME_SWITCH="-f $NUM_FRAMES"
fi

LOGDIR=$(printf "${MOVIE}-s%02d_k%02d-logs" ${NUM_FRAMES} ${KFDIST})

mkdir -p ${LOGDIR}
LOGFILESUFFIX=k${KFDIST}_n${NWORKERS}_o${NOFFSET}_y${YVAL}_$(date +%F-%H:%M:%S)
echo -en "\033]0; ${REGION} ${LOGFILESUFFIX//_/ }\a"
set -u

if [ -z "$SSIM_ONLY" ]; then
    ${MU_ROOT}${XCENC_EXEC}_server.py \
        ${DEBUG} \
        ${UPLOAD} \
        ${FRAME_SWITCH} \
        -n ${NWORKERS} \
        -o ${NOFFSET} \
        -X $((${NWORKERS} / 2)) \
        -Y ${YVAL} \
        -K ${KFDIST} \
        -v ${MOVIE}-4k-y4m"${VID_SUFFIX}" \
        -b excamera-${REGION} \
        -r ${REGION} \
        -l ${FN_NAME[NUM_FRAMES]} \
        -t ${PORTNUM} \
        -h ${PUBLIC_IP} \
        -T ${STATEPORT} \
        -R ${STATETHREADS} \
        -H ${PUBLIC_IP} \
        -O ${LOGDIR}/${XCENC_EXEC}_transitions_${LOGFILESUFFIX}.log \
        -M
fi

if [ $? = 0 ] && [ ! -z "${UPLOAD}" ]; then
    ${MU_ROOT}${DUMP_EXEC}_server.py \
        ${DEBUG} \
        -n ${NWORKERS} \
        -o ${NOFFSET} \
        -X $((${NWORKERS} / 2)) \
        -Y ${YVAL} \
        -K ${KFDIST} \
        -v ${MOVIE}-4k-y4m${FRAME_STR} \
        -b excamera-${REGION} \
        -r ${REGION} \
        -l ${FN_NAME[NUM_FRAMES]} \
        -t ${PORTNUM} \
        -h ${PUBLIC_IP} \
        -O ${LOGDIR}/${DUMP_EXEC}_transitions_${LOGFILESUFFIX}.log \
        -M
fi
