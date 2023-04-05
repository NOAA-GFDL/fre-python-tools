#!/bin/sh

sbatch -A gfdl_f $PWD/clock_with_epmt.sh
rptact 100 6 "squeue -u $USER"
