#!/bin/sh
#SBATCH -A Ian.Laflotte
#SBATCH -n 1
#SBATCH --time=00:05:00

module load epmt

epmt run -a python generate_time_averages.py
