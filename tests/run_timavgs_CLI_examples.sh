#!/bin/bash

# quick shell script that generates time-averaged output of a test file for various tests
# against the generate_time_averages python module

source ./tests/timavgs_CLI_examples.sh

echo ""
echo "__________target files___________"
ls $TESTFILE_DIR/$PP_COMP.????01-????12.$VAR.nc
echo "--------------------------------------------------"

echo "running cdo timavg examples"
out_code=$(cdo_timmean_ex)

return $out_code

#echo "running timavg.csh examples"
#timavgcsh_ex
