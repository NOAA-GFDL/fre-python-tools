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
