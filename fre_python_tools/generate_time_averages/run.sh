#!/bin/bash


infile=atmos.197901-198312.LWP.nc
python generate_time_averages.py -i t/testfiles/$infile -o t/testfiles/${infile}_out -p cdo

#infile=atmos.198401-198812.LWP.nc
#python generate_time_averages.py -i t/testfiles/$infile -o t/testfiles/$infile_out -p cdo
