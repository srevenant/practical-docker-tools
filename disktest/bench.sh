#!/bin/bash

export PATH=$(pwd)/src:$PATH

if [ 0$1 -gt 0 ]; then
    ITERATIONS=$1
else
    ITERATIONS=3
fi

runfio() {
    label=$1
    shift

    echo "--- Starting benchmark: $label"
    rm -f results/$label* # clear old #'s

    echo -n "    warmup"
    _fio results/$label-warmup.log "$@"
    x=1
    while [ $x -le $ITERATIONS ]; do
        echo -n "    iter-$x"
        _fio results/$label-run$x.log "$@"
        let x++
    done
}

_fio() {
    log=$1
    shift
    echo " >> fio $@ > $log 2>&1"
    fio "$@" > $log 2>&1
}

runfio vol1-named --directory=/vol1-named ./cfg/duress.fio
runfio vol2-bind --directory=/vol2-bind ./cfg/duress.fio
runfio vol3-local --directory=/vol3-local ./cfg/duress.fio

if [ -e /dev/sdd ]; then
    runfio vol3-raw --filename=/dev/sdd ./cfg/duress.fio
fi
