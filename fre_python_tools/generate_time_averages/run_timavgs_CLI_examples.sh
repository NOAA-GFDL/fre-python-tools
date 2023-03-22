#!/bin/bash

# this is me trying to learn to use `timavg.csh` "by hand". this script should be sourced
# not really doing it by hand, just hate typing things over and over.
# instead, just gonna source+edit+see what happens + repeat until I have ascript
# that seems to average files sensibly.

# then, we're gonna figure out how to intelligently structure it in python.
TARGETDIR=/archive/Ciheim.Brown/am5/2022.01/c96L33_am5f1a0r0_amip/gfdl.ncrc4-intel21-prod-openmp/pp/atmos/ts/monthly/5yr
PP_COMP=atmos
VAR=LWP

echo ""
echo "__________target files___________"
ls $TARGETDIR/$PP_COMP.????01-????12.$VAR.nc
echo "--------------------------------------------------"
source ./timavgs_CLI_examples.sh

##looks good but maybe not done here?
#echo "running timavg.csh examples"
#timavgcsh_ex

##looks good but maybe not done here?
#echo "running cdo timavg examples"
#cdo_timavg_ex

##looks good but maybe not done here?
##WOAH this is much faster than timavg...
#echo "running cdo timmean examples"
#cdo_timmean_ex

#under construction...
#echo "running ncclimo timavg examples"
#ncclimo_timavg_ex
