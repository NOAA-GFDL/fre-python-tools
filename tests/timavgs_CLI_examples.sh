#!/bin/bash

PP_COMP=atmos
VAR=LWP
TESTFILE_DIR=./tests/time_avg_test_files
TESTFILE=$TESTFILE_DIR/${PP_COMP}.197901-198312.${VAR}.nc

#cdo timavg
function cdo_timmean_ex(){

	#avg the variable at each lat/lon point over each month --> 12 #'s per lat/lon point (one per month)
	outfile=$TESTFILE_DIR/cdo_ymonmean_CLI_test_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	cdo ymonmean $TESTFILE $outfile
	unset outfile

	## avg the variable at each lat/lon point over each season --> four # per lat/lon point 
	outfile=$TESTFILE_DIR/cdo_yseasmean_CLI_test_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	cdo yseasmean $TESTFILE $outfile
	unset outfile
	
	## avg the variable at each lat/lon point over all points in time --> one # per lat/lon point 
	outfile=$TESTFILE_DIR/cdo_timmean_CLI_test_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	cdo timmean $TESTFILE $outfile	

	return 0
}

## i like this idea to create a comfortable benchmark...
## but i already know cdo can bitwise reproduce the result
## worse, i'd need to include this in the conda env.
## comment out for now.
## using FRE-NCtools' timavg.csh
#function timavgcsh_ex(){
#	module load fre-nctools	
#
#	outfile=$TESTFILE_DIR/timavgcsh_CLI_test_${PP_COMP}_${VAR}_1979_5y.nc
#	if [ -f $outfile ] ; then rm $outfile ; fi
#	timavg.csh -r8 -mb -o $outfile $TESTFILE
#
#	module unload fre-nctools	
#	return
#}

