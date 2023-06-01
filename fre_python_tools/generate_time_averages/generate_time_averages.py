#!/usr/bin/env python
''' tools for generating time averages from various packages '''

import sys
import argparse
import math
from subprocess import Popen, PIPE

import numpy
from netCDF4 import Dataset

def generate_frepythontools_timavg(infile=None, outfile=None,
                                   do_weighted_avg=True, do_std_dev=True):
    ''' my own time-averaging function. mostly an exercise. '''
    if __debug__:
        print('calling generate_frepythontools_timavg for file: ' + infile)

    exitstatus=1
    var=infile.split('/').pop().split('.')[-2]
    if __debug__:
        print(f'var={var}')

    nc_fin = Dataset(infile, 'r')

    # check for the variable we're hoping is in the file
    fin_vars=nc_fin.variables
    for key in fin_vars:
        if str(key)==var:
            time_bnds=nc_fin['time_bnds'][:].copy()
            key_found=True
            break
    if not key_found:
        print('requested variable not found. exit.')
        return exitstatus


    # check for mask (will be important for later dev stages)
    #is_masked = ma.is_masked(val_array)

    # read in sizes of specific axes
    fin_dims =nc_fin.dimensions
    lat_bnd=fin_dims['lat'].size
    lon_bnd=fin_dims['lon'].size
    time_bnd=fin_dims['time'].size

    # initialize arrays
    avgvals=numpy.zeros((1,lat_bnd,lon_bnd),dtype=float)
    if do_std_dev:
        stddevs=numpy.zeros((1,lat_bnd,lon_bnd),dtype=float)

    # compute average, for each lat/lon coordinate over time record in file
    for lon in range(lon_bnd):
        if lon%32 == 0:
            print(f'lon # {lon+1}/{lon_bnd}')

        for lat in range(lat_bnd):
            val_array= numpy.moveaxis( nc_fin[var][:], 0, -1 )[lat][lon].copy()

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


    ## write output file here
    nc_fout = Dataset( outfile, 'w',persist=True)
    nc_fout.close()
    return 0


# must have fre-nctools, which is not included in the conda env by default.
def generate_frenctools_timavg(infile=None, outfile=None, do_weighted_avg=True, do_std_dev=True):
    ''' use fre-nctool's CLI timavg.csh with subprocess call '''
    if __debug__:
        print(f'calling generate_frenctools_timavg for file: {infile}')

    precision='-r8'
    timavgcsh_command=['timavg.csh', precision, '-mb','-o', outfile, infile]
    exitstatus=1

    with Popen(timavgcsh_command,
               stdout=PIPE, stderr=PIPE, shell=False) as subp:
        output=subp.communicate()[0]
        print(f'output={output}')

        if subp.returncode < 0:
            print('error')
            exitstatus=1
        else:
            print('success')
            exitstatus=0

    return exitstatus


def generate_cdo_timavg(infile=None, outfile=None, avg_type=None):
    ''' use cdo's python module for time-averaging '''
    if __debug__:
        print(f'calling generate_cdo_timavg for file: {infile}')
        print(f'outfile={outfile}')
        print(f'avg_type={avg_type}')

    if all([avg_type!='all',avg_type!='seas',avg_type!='month']):
        print(f'ERROR, avg_type requested unknown.')
        return 1

    from cdo import Cdo
    _cdo=Cdo()
    
    if avg_type == 'all':
        print(f'time-averaging requested.')
        _cdo.timmean(input=infile, output=outfile, returnCdf=True)
        print(f'time averaging requested')
    elif avg_type == 'seas':
        print(f'seasonal time-averaging requested.')
        _cdo.yseasmean(input=infile, output=outfile, returnCdf=True)
        print(f'done averaging over seasons')
    elif avg_type == 'month':
        print(f'time-averaging requested.')
        _cdo.ymonmean(input=infile, output=outfile, returnCdf=True)
        print(f'done averaging over months')
    else:
        print(f'problem.')
        return 1

    print(f'done averaging')

    return 0


def generate_time_average(pkg=None, infile=None, outfile=None, avg_type=None):
    ''' steering function to various averaging functions above'''
    if __debug__:
        print(f'calling generate time averages for file: {infile}')
    exitstatus=1

    #needs a case statement
    if   pkg == 'cdo'            :
        exitstatus=generate_cdo_timavg(            infile=infile, outfile=outfile, avg_type=avg_type )
    elif pkg == 'fre-nctools'    :
        exitstatus=generate_frenctools_timavg(     infile=infile, outfile=outfile )
    elif pkg == 'fre-python-tools':
        exitstatus=generate_frepythontools_timavg( infile=infile, outfile=outfile )
    else                         :
        print('requested package unknown. exit.')
        exitstatus=1

    return exitstatus

def main():
    ''' main, for steering, when called like `python generate_time_averages.py` '''
    argparser = argparse.ArgumentParser(
        description='generate time averages for specified set of netCDF files. Example: \
        generate-time-averages.py /path/to/your/files/')
    argparser.add_argument('inf',
                           help='input file name',
                           type=str)
    argparser.add_argument('outf',
                           help='output file name',
                           type=str)
    argparser.add_argument('-p','--pkg',
                          help='package to use for timavg [e.g. cdo, fre-nctools, fre-python-tools]',
                          type=str, default='cdo')
    argparser.add_argument('-a','--avg',
                           help='type of time average to generate [e.g. month,seas,all]',
                          type=str, default='all')
    cli_args = argparser.parse_args()
    generate_time_average( cli_args.pkg, cli_args.inf, cli_args.outf, cli_args.avg )


if __name__ == '__main__':
    import time
    import sys
    start_time=time.perf_counter()
    main(sys.argv[1:])
    finish_time=time.perf_counter()
    print(f'Finished in total time {round(finish_time - start_time , 2)} second(s)')
