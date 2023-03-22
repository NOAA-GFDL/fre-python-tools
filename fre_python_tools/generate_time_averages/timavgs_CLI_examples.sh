#!/bin/sh

#timavg.csh
function timavgcsh_ex(){
	module load fre-nctools
	
	if [ -f timavgcsh_test1979_5y.nc ] ; then rm timavgcsh_test1979_5y.nc ; fi
	timavg.csh -r8 -mb -o ./timavgcsh_test1979_5y.nc $TARGETDIR/$PP_COMP.197901-198312.$VAR.nc
	
	if [ -f timavgcsh_test1984_5y.nc ] ; then rm timavgcsh_test1984_5y.nc ; fi										 
	timavg.csh -r8 -mb -o ./timavgcsh_test1984_5y.nc $TARGETDIR/$PP_COMP.198401-198812.$VAR.nc

	return
}

#cdo timavg
function cdo_timavg_ex(){
	module load cdo

	if [ -f cdo_timavg_test1979_5y.nc ] ; then rm cdo_timavg_test1979_5y.nc ; fi
	cdo timavg $TARGETDIR/$PP_COMP.197901-198312.$VAR.nc ./cdotimavg_test1979_5y.nc
	
	if [ -f cdo_timavg_test1984_5y.nc ] ; then rm cdo_timavg_test1984_5y.nc ; fi										 
	cdo timavg $TARGETDIR/$PP_COMP.198401-198812.$VAR.nc ./cdotimavg_test1984_5y.nc

	return
}

# is this the same as `cdo timavg` ? if so, why does it exist?
# looks like a separate function call from what i can tell,
# e.g. not an alias to `timavg`
#cdo timmean
function cdo_timmean_ex(){
	module load cdo

	if [ -f cdo_timmean_test1979_5y.nc ] ; then rm cdo_timmean_test1979_5y.nc ; fi
	cdo timmean $TARGETDIR/$PP_COMP.197901-198312.$VAR.nc ./cdotimmean_test1979_5y.nc
	
	if [ -f cdo_timmean_test1984_5y.nc ] ; then rm cdo_timmean_test1984_5y.nc ; fi										 
	cdo timmean $TARGETDIR/$PP_COMP.198401-198812.$VAR.nc ./cdotimmean_test1984_5y.nc

	return
}


function nco_ncclimo_ex(){
	module load nco

	ncclimo

	# ????

	return
}



