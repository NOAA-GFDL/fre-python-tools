#!/usr/bin/env python
''' tools for generating time averages from various packages '''

#import time
import argparse
import math
from subprocess import Popen, PIPE
import numpy
from numpy import ma

from netCDF4 import Dataset
from cdo import Cdo


def generate_frepythontools_timavg(targpath=None, outfile=None, var=None,
                                   debug_mode=False, do_weighted_avg=True, do_std_dev=True):
    ''' my own time-averaging function. mostly an exercise. '''
    if debug_mode:
        print("calling generate_frepythontools_timavg for file: " + targpath)

    nc_fin = Dataset(targpath, "r")
    
    # check for the variable we're hoping is in the file
    fin_vars=nc_fin.variables
    for key in fin_vars:
        if str(key)==var:
            time_bnds=nc_fin['time_bnds'][:]
            key_found=True
            break
    if not key_found:
        print('requested variable not found. exit.')
        return

    # check for mask (will be important for later dev stages)
    #is_masked = ma.is_masked(val_array)
    #print(f'is_masked={is_masked}')

    # read in sizes of specific axes
    fin_dims =nc_fin.dimensions
    lat_bnd=fin_dims['lat'].size
    lon_bnd=fin_dims['lon'].size
    time_bnd=fin_dims['time'].size
    
    # initialize arrays
    avgvals=numpy.zeros((1,lat_bnd,lon_bnd),dtype=float)
    if do_std_dev:
        stddevs=numpy.zeros((1,lat_bnd,lon_bnd),dtype=float)

    ### is a 3-d array.
    ### val[time][lat][lon]
    #val_array=nc_fin[var][:]

    # compute average, for each lat/lon coordinate over time record in file
    for lat in range(lat_bnd):
        for lon in range(lon_bnd):

            val_array= numpy.reshape( nc_fin[var][:], (0, -1) )[lat][lon]
            print(val_array)
            assert(False)
            if do_weighted_avg:                
                time_bnd_sum = sum( (time_bnds[tim][1] - time_bnds[tim][0]) for tim in range(time_bnd))
                avgvals[0][lat][lon]=sum( val_array[tim][lat][lon] * (
                                                      time_bnds[tim][1]-time_bnds[tim][0]
                                                              ) for tim in range(time_bnd) ) / time_bnd_sum
                if do_std_dev: #std dev *of the mean*. not a vanilla std dev.
                    stddevs[0][lat][lon]=math.sqrt(
                                                 sum(
                        (val_array[tim][lat][lon]-avgvals[0][lat][lon]) ** 2.
                                                     for tim in range(time_bnd)
                                                    )
                                                  ) / time_bnd_sum

            else: #unweighted average/stddev
                avgvals[0][lat][lon]=sum( # no time sum needed here, b.c. unweighted, so sum
                    val_array[tim][lat][lon] for tim in range(time_bnd)
                                        ) / time_bnd

                if do_std_dev:
                    stddevs[0][lat][lon]=math.sqrt(
                                                 sum(
                                          (val_array[tim][lat][lon]-avgvals[0][lat][lon]) ** 2.
                                                     for tim in range(time_bnd)
                                                    ) / ( (time_bnd - 1. ) * time_bnd )
                                                  )

    #finish_time=time.perf_counter()
    #print("\n done with important part of generate_frepythontools_timavg")
    #print(f'Finished the important part in {round(finish_time - start_time , 2)} second(s)')

    # for checking the averaging i do against the averaging timavg.csh does
    nc_compare=Dataset( ('timavgcsh_atmos_LWP_test1979_5y.nc'), 'r')
    compare_avgvals=nc_compare[var][:]

    if do_std_dev:
        print(
        f'avgvals[0][0][0]        = \
        {avgvals[0][0][0]} +/- {stddevs[0][0][0]}'  )
        print(f'type(stddevs[0][0][0])={type(stddevs[0][0][0])}')
    else:
        print(
        f'avgvals[0][0][0]        = \
        {avgvals[0][0][0]}'  )
    print(f'type(avgvals[0][0][0])={type(avgvals[0][0][0])}')
    print(
        f'compare_avgvals[0][0][0]= \
        {compare_avgvals[0][0][0]}'    )

    ## write output file here
    nc_fout = Dataset( outfile, 'w',persist=True)
    nc_fout.close()
    return


# must have done something like `module load fre-nctools`
def generate_frenctools_timavg(targpath=None, outfile=None, debug_mode=False):
    ''' use fre-nctool's CLI timavg.csh with subprocess call '''
    if debug_mode:
        print(f'calling generate_frenctools_timavg for file: {targpath}')

    #Popen(['timavg.csh','-r8','-mb','-o', outfile, targpath],
    #      stdout=PIPE, stderr=PIPE, shell=False)

    with Popen(['timavg.csh','-r8','-mb','-o', outfile, targpath],
               stdout=PIPE, stderr=PIPE, shell=False) as subp:
        output=subp.communicate()[0]
        print(f'output={output}')

        if subp.returncode < 0:
            print('error')

    return

# under construction
def generate_nco_timavg(targpath=None, outfile=None, debug_mode=False):
    ''' use nco python module for time-averaging '''
    if debug_mode:
        print(f'calling generate_nco_timavg for file: {targpath}')
        print(f'output file: {outfile}')
    #targpath=targdir+targfile    targoutpath=outfile

    #from nco import ncclimo
    print('under construction.')
    return

# must be in conda env with pip-installed cdo package (`pip install cdo --user`)
def generate_cdo_timavg(targpath=None, outfile=None, debug_mode=False):
    ''' use cdo's python module for time-averaging '''
    if debug_mode:
        print(f'calling generate_cdo_timavg for file: {targpath}')

    cdo=Cdo()
    cdo.timavg(input=targpath, output=outfile, returnCdf=True)

    return

def generate_time_average(pkg=None, targpath=None, outfile=None, debug_mode=False):
    ''' steering function to various averaging functions above'''
    if debug_mode:
        print(f'calling generate time averages for file: {targpath}')

    #needs a case statement
    if   pkg == "cdo"            :
        generate_cdo_timavg(            targpath, outfile, debug_mode )
    elif pkg == "nco"            :
        generate_nco_timavg(            targpath, outfile, debug_mode )
    elif pkg == "fre-nctools"    :
        generate_frenctools_timavg(     targpath, outfile, debug_mode )
    elif pkg == "fre-pythontools":
        generate_frepythontools_timavg( targpath, outfile, 'LWP', debug_mode )
    else                         :
        print('requested package unknown. exit.')

    return

def main():
    ''' main, for steering, when called like `python generate_time_averages.py` '''
    debug_mode=True

    ## argument parser TO DO
    comp='atmos'
    #VAR='droplets'
    var='LWP'

    targdir='./testfiles/'
    targfile1=comp+'.197901-198312.'+var+'.nc'
    #targfile2=COMP+'.198401-198812.'+VAR+'.nc'

    # argparsing aspect still under construction
    argparser = argparse.ArgumentParser(
        description="generate time averages for specified set of netCDF files. Example: \
        generate-time-averages.py /path/to/your/files/")

    #### every ArgumentParser comes with it's '-h' and '--help' flags pre-defined.
    #### if i redefine a flag that already exists, get a "conflicting option string" error
    argparser.add_argument('-o', '--outf',
                           help="output file name", type=str)
    argparser.add_argument('-i', '--inf',
                           help="input file name", type=str)
    argparser.add_argument('-c', '--comp',
                           help="input model component of input file name", type=str)
    argparser.add_argument('-v', '--var',
                           help="variable from input to average", type=str)
    #cli_args = argparser.parse_args()
    #print(cli_args.outf)    #print(cli_args.inf)    #print('cli_args={cli_args}')

    ## ----------------- cdo timavg calls
    #generate_time_average( 'cdo', targdir+targfile1,
    #                       'test_cdo_pypi_1.nc', debug_mode)
    #generate_time_average( 'cdo', targdir+targfile2,
    #                       'test_cdo_pypi_2.nc', debug_mode)

    ## ------------------ fre-nctools timavg.csh calls
    #generate_time_average( 'fre-nctools', targdir+targfile1,
    #                       'test_frenc_pypi_1.nc', debug_mode)
    #generate_time_average( 'fre-nctools', targdir+targfile2,
    #                       'test_frenc_pypi_2.nc', debug_mode)

    # ------------------ fre-python-tools gen time average calls
    generate_time_average( 'fre-pythontools', targdir+targfile1,
                           'test_frenc_pypi_1.nc', debug_mode)
    #generate_time_average( 'fre-python-tools', targdir+targfile2,
    #                       'test_frenc_pypi_2.nc', debug_mode)

    return

#entry point for CLI usage, mainly for prototyping at this time.
if __name__ == "__main__":
    import time
    print('calling main())')
    start_time=time.perf_counter()
    main()
    finish_time=time.perf_counter()
    print('\n done calling main()')
    print(f'Finished in total time {round(finish_time - start_time , 2)} second(s)')
