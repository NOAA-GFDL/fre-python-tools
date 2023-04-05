#!/bin/sh -l
#SBATCH --job-name=epmt_gentimeaverage
#SBATCH -A Ian.Laflotte
#SBATCH --ntasks 1
#SBATCH --nodes 1
#SBATCH --time=30
#SBATCH --output=clock_with_epmt.out

module purge
#module load slurm
module load python
module load epmt
module list

set -x 

#epmt run -a python generate_time_averages.py

epmt start
eval `epmt source`
python generate_time_averages.py
epmt stop
f=`epmt stage`
epmt submit $f

#python generate_time_averages.py
