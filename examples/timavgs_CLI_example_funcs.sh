#!/bin/bash

function cdo_timavg_exs(){ #all of these are unweighted. extra steps required for weighted.

	
	#### averages ####
	
	## avg the variable at each lat/lon point over each month --> 12 #'s per lat/lon point (one per month)
	outfile=$TESTFILE_DIR/cdo_ymonavg_CLI_test_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	cdo ymonavg $TESTFILE $outfile
	unset outfile
	
	## avg the variable at each lat/lon point over each season --> four # per lat/lon point 
	outfile=$TESTFILE_DIR/cdo_yseasavg_CLI_test_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	cdo yseasavg $TESTFILE $outfile
	unset outfile
	
	## avg the variable at each lat/lon point over all points in time --> one # per lat/lon point 
	outfile=$TESTFILE_DIR/cdo_timavg_CLI_test_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	cdo -b F64 timavg $TESTFILE $outfile
	ls $outfile
	unset outfile

	
	#### stddev ####

	## stddev of variable at each lat/lon point over each month --> 12 #'s per lat/lon point (one per month)
	outfile=$TESTFILE_DIR/cdo_ymonstd_CLI_test_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	cdo ymonstd $TESTFILE $outfile
	unset outfile
	
	## stddev of variable at each lat/lon point over each season --> four # per lat/lon point 
	outfile=$TESTFILE_DIR/cdo_yseasstd_CLI_test_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	cdo yseasstd $TESTFILE $outfile
	unset outfile
	
	## stddev of variable at each lat/lon point over all points in time --> one # per lat/lon point 
	outfile=$TESTFILE_DIR/cdo_timstd_CLI_test_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	cdo -b F64 timstd $TESTFILE $outfile
	ls $outfile
	unset outfile

	
	#### stddev (N-1) ####
	
	## stddev1 of variable at each lat/lon point over each month --> 12 #'s per lat/lon point (one per month)
	outfile=$TESTFILE_DIR/cdo_ymonstd1_CLI_test_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	cdo ymonstd1 $TESTFILE $outfile
	unset outfile
	
	## stddev1 of variable at each lat/lon point over each season --> four # per lat/lon point 
	outfile=$TESTFILE_DIR/cdo_yseasstd1_CLI_test_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	cdo yseasstd1 $TESTFILE $outfile
	unset outfile
	
	## stddev1 of variable at each lat/lon point over all points in time --> one # per lat/lon point 
	outfile=$TESTFILE_DIR/cdo_timstd1_CLI_test_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	cdo -b F64 timstd1 $TESTFILE $outfile
	ls $outfile
	unset outfile

	return 0
}

function fre_nctools_timavg_exs(){
	#if you already have fre-nctools, this step is unnecessary
	module load fre-nctools

	outfile=$TESTFILE_DIR/fre_nctools_timavg_CLI_test_r8_mb_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	timavg.csh -d -r8 -mb -o $outfile $TESTFILE
	ls $outfile
	unset outfile

	outfile=$TESTFILE_DIR/fre_nctools_timavg_CLI_test_r8_b_${PP_COMP}_${VAR}_1979_5y.nc
	if [ -f $outfile ] ; then rm -f $outfile ; fi
	timavg.csh -r8 -b -o $outfile $TESTFILE
	ls $outfile
	unset outfile

	return 0
}
