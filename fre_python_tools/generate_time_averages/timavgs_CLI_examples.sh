#!/bin/sh

#timavg.csh
function timavgcsh_ex(){
	module load fre-nctools
	
	if [ -f timavgcsh_test1979_5y.nc ] ; then rm timavgcsh_test1979_5y.nc ; fi
	timavg.csh -r8 -mb -o ./timavgcsh_${PP_COMP}_${VAR}_test1979_5y.nc $TARGETDIR/${PP_COMP}.197901-198312.${VAR}.nc
	
	if [ -f timavgcsh_test1984_5y.nc ] ; then rm timavgcsh_test1984_5y.nc ; fi										 
	timavg.csh -r8 -mb -o ./timavgcsh_${PP_COMP}_${VAR}_test1984_5y.nc $TARGETDIR/${PP_COMP}.198401-198812.${VAR}.nc

	return
}

#local timavg.csh
function local_timavgcsh_ex(){
	module load fre-nctools
	
	if [ -f timavgcsh_test1979_5y.nc ] ; then rm timavgcsh_test1979_5y.nc ; fi
	./timavg.csh -r8 -mb -o ./timavgcsh_${PP_COMP}_${VAR}_test1979_5y.nc $TARGETDIR/${PP_COMP}.197901-198312.${VAR}.nc
	
  	#if [ -f timavgcsh_test1984_5y.nc ] ; then rm timavgcsh_test1984_5y.nc ; fi  
 	#./timavg.csh -r8 -mb -o ./timavgcsh_${PP_COMP}_${VAR}_test1984_5y.nc $TARGETDIR/${PP_COMP}.198401-198812.${VAR}.nc

	return
}

#cdo timavg
function cdo_timavg_ex(){
	module load cdo

	##avg the variable at each lat/lon point over all points in time --> one # per lat/lon point 
	cdo timavg $TARGETDIR/${PP_COMP}.197901-198312.${VAR}.nc ./cdo_timavg_${PP_COMP}_${VAR}_test1979_5y.nc
	cdo timavg $TARGETDIR/${PP_COMP}.198401-198812.${VAR}.nc ./cdo_timavg_${PP_COMP}_${VAR}_test1984_5y.nc
	return
	#avg the variable at each lat/lon point over each season --> four #'s per lat/lon point (one per season)
	cdo yseasavg $TARGETDIR/${PP_COMP}.197901-198312.${VAR}.nc ./cdo_yseasavg_${PP_COMP}_${VAR}_test1979_5y.nc
	cdo yseasavg $TARGETDIR/${PP_COMP}.198401-198812.${VAR}.nc ./cdo_yseasavg_${PP_COMP}_${VAR}_test1984_5y.nc
	
	#avg the variable at each lat/lon point over each month --> 12 #'s per lat/lon point (one per month)
	cdo ymonavg $TARGETDIR/${PP_COMP}.197901-198312.${VAR}.nc ./cdo_ymonavg_${PP_COMP}_${VAR}_test1979_5y.nc
	cdo ymonavg $TARGETDIR/${PP_COMP}.198401-198812.${VAR}.nc ./cdo_ymonavg_${PP_COMP}_${VAR}_test1984_5y.nc


	return
}

## is this the same as `cdo timavg` ? if so, why does it exist?
## looks like a separate function call from what i can tell,
## e.g. not an alias to `timavg` --> WRONG it is an alias
##cdo timmean
#function cdo_timmean_ex(){
#	module load cdo
#
#	if [ -f cdo_timmean_test1979_5y.nc ] ; then rm cdo_timmean_test1979_5y.nc ; fi
#	cdo timmean $TARGETDIR/${PP_COMP}.197901-198312.${VAR}.nc ./cdo_timmean_${PP_COMP}_${VAR}_test1979_5y.nc
#	
#	if [ -f cdo_timmean_test1984_5y.nc ] ; then rm cdo_timmean_test1984_5y.nc ; fi										 
#	cdo timmean $TARGETDIR/${PP_COMP}.198401-198812.${VAR}.nc ./cdo_timmean_${PP_COMP}_${VAR}_test1984_5y.nc
#
#	return
#}


#function nco_ncclimo_ex(){
#	module load nco
#
#	ncclimo
#
#	# ????
#
#	return
#}



