#!/bin/sh

nohup ./forked.sh &

exec ./sigtest.py
