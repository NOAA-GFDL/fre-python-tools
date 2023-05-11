#!/bin/sh

# quick shell script that generates time-averaged output of a test file for various tests
# against the generate_time_averages python module

source timavgs_CLI_examples.sh

echo ""
echo "__________target files___________"
ls $TARGETDIR/$PP_COMP.????01-????12.$VAR.nc
echo "--------------------------------------------------"
source ./timavgs_CLI_examples.sh

echo "running cdo timavg examples"
cdo_timmean_ex

#echo "running timavg.csh examples"
#timavgcsh_ex
