#!/usr/bin/env python
''' tools for generating time averages from various packages '''

#import time
import sys
import argparse
import math
from subprocess import Popen, PIPE
#from psutil import Process

import numpy
#from numpy import ma

from netCDF4 import Dataset
from cdo import Cdo

#@profile
def generate_frepythontools_timavg(targpath=None, outfile=None, var=None,
                                   do_weighted_avg=True, do_std_dev=True):
    ''' my own time-averaging function. mostly an exercise. '''
    if __debug__:
        print("calling generate_frepythontools_timavg for file: " + targpath)

    #mem=Process().memory_info().rss/(1.e+6) #memory size in bytes
    #rssmem=Process().memory_info().rss/(1.e+6) #memory size in bytes
    #vmsmem=Process().memory_info().vms/(1.e+6) #memory size in bytes
    #print(f'rss/vms memory use pre-opening nc file: {rssmem} / {vmsmem} Mb')
    nc_fin = Dataset(targpath, "r")
    #print(f'rss memory use after-opening nc file: {Process().memory_info().rss/1.e+6} Mb, \
    #diff from init is {(Process().memory_info().rss/1.e+6)-rssmem} Mb')
    #print(f'vms memory use after-opening nc file: {Process().memory_info().vms/1.e+6} Mb, \
    #diff from init is {(Process().memory_info().vms/1.e+6)-vmsmem} Mb')

    #sys.exit()
    
    # check for the variable we're hoping is in the file
    fin_vars=nc_fin.variables
    for key in fin_vars:
        if str(key)==var:
            time_bnds=nc_fin['time_bnds'][:].copy()
            key_found=True
            #print(f'memory use after nc_fin[\'timebnds\'][:]: {Process().memory_info().rss/100000.} Mb, \
            #diff from init is {(Process().memory_info().rss-mem)/(1.e+6)} Mb')
            break
    if not key_found:
        print('requested variable not found. exit.')
        assert False
        sys.exit()


    # check for mask (will be important for later dev stages)
    #is_masked = ma.is_masked(val_array)
    #print(f'is_masked={is_masked}')

    # read in sizes of specific axes
    fin_dims =nc_fin.dimensions
    lat_bnd=fin_dims['lat'].size
    lon_bnd=fin_dims['lon'].size
    time_bnd=fin_dims['time'].size
    #print(f'memory use after fin.dimensions + sizes: {Process().memory_info().rss/100000.} Mb, \
    #diff from init is {(Process().memory_info().rss-mem)/(1.e+6)} Mb')

    # initialize arrays
    avgvals=numpy.zeros((1,lat_bnd,lon_bnd),dtype=float)
    if do_std_dev:
        stddevs=numpy.zeros((1,lat_bnd,lon_bnd),dtype=float)

    #print(f'memory use after ndarray initialization with zeros: {Process().memory_info().rss/100000.} Mb, \
    #diff from init is {(Process().memory_info().rss-mem)/(1.e+6)} Mb')

    ### is a 3-d array.
    ### val[time][lat][lon]
    #val_array=nc_fin[var][:]

    # compute average, for each lat/lon coordinate over time record in file
    count=0
    for lon in range(lon_bnd):
        if lon%32 == 0:
            print(f'lon # {lon+1}/{lon_bnd}')

        for lat in range(lat_bnd):
            count+=1
            # copy keeps the memory use lighter...
            # diff from init memory went from ~21 Mb --> 8.6 Mb when i added copy.
            val_array= numpy.moveaxis( nc_fin[var][:], 0, -1 )[lat][lon].copy()
            #val_array= numpy.moveaxis( nc_fin[var][:], 0, -1 )[lat][lon]

            #if lat%30 == 0:
            #    print(f'(lat #{lat+1}/{lat_bnd}) memory use after copy of slice of value array: {Process().memory_info().rss/100000.} Mb, \
            #    diff from init is {(Process().memory_info().rss-mem)/(1.e+6)} Mb')


            if do_weighted_avg:
                time_bnd_sum = sum( (time_bnds[tim][1] - time_bnds[tim][0]) for tim in range(time_bnd))
                avgvals[0][lat][lon]=sum( val_array[tim] * (
                                                      time_bnds[tim][1]-time_bnds[tim][0]
                                                              ) for tim in range(time_bnd) ) / time_bnd_sum
                if do_std_dev: #std dev *of the mean*. not a vanilla std dev.
                    stddevs[0][lat][lon]=math.sqrt(
                                                 sum(
                        (val_array[tim]-avgvals[0][lat][lon]) ** 2.
                                                     for tim in range(time_bnd)
                                                    )
                                                  ) / time_bnd_sum

            else: #unweighted average/stddev
                avgvals[0][lat][lon]=sum( # no time sum needed here, b.c. unweighted, so sum
                    val_array[tim] for tim in range(time_bnd)
                                        ) / time_bnd

                if do_std_dev:
                    stddevs[0][lat][lon]=math.sqrt(
                                                 sum(
                                          (val_array[tim]-avgvals[0][lat][lon]) ** 2.
                                                     for tim in range(time_bnd)
                                                    ) / ( (time_bnd - 1. ) * time_bnd )
                                                  )
            del val_array
            if count > 3600: break
            #break
        if count > 3600: break
        #break

    #finish_time=time.perf_counter()
    print("\n done with important part of generate_frepythontools_timavg")
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
    #return


# must have done something like `module load fre-nctools`
def generate_frenctools_timavg(targpath=None, outfile=None):
    ''' use fre-nctool's CLI timavg.csh with subprocess call '''
    if __debug__:
        print(f'calling generate_frenctools_timavg for file: {targpath}')

    #Popen(['timavg.csh','-r8','-mb','-o', outfile, targpath],
    #      stdout=PIPE, stderr=PIPE, shell=False)

    with Popen(['timavg.csh','-r8','-mb','-o', outfile, targpath],
               stdout=PIPE, stderr=PIPE, shell=False) as subp:
        output=subp.communicate()[0]
        print(f'output={output}')

        if subp.returncode < 0:
            print('error')

    #return

# under construction
def generate_nco_timavg(targpath=None, outfile=None):
    ''' use nco python module for time-averaging '''
    if __debug__:
        print(f'calling generate_nco_timavg for file: {targpath}')
        print(f'output file: {outfile}')
    #targpath=targdir+targfile    targoutpath=outfile

    #from nco import ncclimo
    print('under construction.')
    #return

# must be in conda env with pip-installed cdo package (`pip install cdo --user`)
def generate_cdo_timavg(targpath=None, outfile=None):
    ''' use cdo's python module for time-averaging '''
    if __debug__:
        print(f'calling generate_cdo_timavg for file: {targpath}')

    cdo=Cdo()
    cdo.timavg(input=targpath, output=outfile, returnCdf=True)

    #return

def generate_time_average(pkg=None, targpath=None, outfile=None):
    ''' steering function to various averaging functions above'''
    if __debug__:
        print(f'calling generate time averages for file: {targpath}')

    #needs a case statement
    if   pkg == "cdo"            :
        generate_cdo_timavg(            targpath, outfile )
    elif pkg == "nco"            :
        generate_nco_timavg(            targpath, outfile )
    elif pkg == "fre-nctools"    :
        generate_frenctools_timavg(     targpath, outfile )
    elif pkg == "fre-pythontools":
        generate_frepythontools_timavg( targpath, outfile, 'LWP' )
    else                         :
        print('requested package unknown. exit.')

    #return

def main():
    ''' main, for steering, when called like `python generate_time_averages.py` '''

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
    #                       'test_cdo_pypi_1.nc')
    #generate_time_average( 'cdo', targdir+targfile2,
    #                       'test_cdo_pypi_2.nc')

    ## ------------------ fre-nctools timavg.csh calls
    #generate_time_average( 'fre-nctools', targdir+targfile1,
    #                       'test_frenc_pypi_1.nc')
    #generate_time_average( 'fre-nctools', targdir+targfile2,
    #                       'test_frenc_pypi_2.nc')

    # ------------------ fre-python-tools gen time average calls
    generate_time_average( 'fre-pythontools', targdir+targfile1,
                           'test_frenc_pypi_1.nc')
    #generate_time_average( 'fre-python-tools', targdir+targfile2,
    #                       'test_frenc_pypi_2.nc')

    #return

#entry point for CLI usage, mainly for prototyping at this time.
if __name__ == "__main__":
    import time
    print('calling main())')
    start_time=time.perf_counter()
    main()
    finish_time=time.perf_counter()
    print('\n done calling main()')
    print(f'Finished in total time {round(finish_time - start_time , 2)} second(s)')
