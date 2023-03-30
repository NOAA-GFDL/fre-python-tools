#!/usr/bin/env python

import argparse
import time
#import os, sys
#import netCDF4 as nc


def generate_frepythontools_timavg(targdir=None, targfile=None, outfile=None, var=None, debugMode=False):
    if debugMode: print("calling generate_frepythontools_timavg for file: " + targdir + targfile)

    import netCDF4 as nc
    do_weighted_avg=True
    #do_std_dev=True
    
    nc_fin = nc.Dataset((targdir+targfile), "r")
    fin_vars=nc_fin.variables

    ### is a 3-d array.
    ### val[time][lat][lon]
    val_array=[]
    time_bnds=[]
    for key in fin_vars:
        if (str(key)==var):
            val_array=nc_fin[key][:]
            time_bnds=nc_fin['time_bnds'][:]
            break

    fin_dims =nc_fin.dimensions
    time_bnd=fin_dims['time'].size
    lat_bnd=fin_dims['lat'].size
    lon_bnd=fin_dims['lon'].size
    #print(val_array[time_bnd-1][lat_bnd-1][lon_bnd-1])
    print('time_bnds type is: ' + str(type(time_bnds[0][0])))  #numpy.float64
    print('val_array type is: ' + str(type(val_array[0][0][0]))) #numpy.float32
    avgvals=[[[0. for lon in range(lon_bnd)] for lat in range(lat_bnd)] for time in range(1)]
    print('avgvals type is: '+str(type(avgvals[0][0][0])))
    #assert(False)


    for lat in range(lat_bnd):
        for lon in range(lon_bnd):

            if do_weighted_avg:
                avgvals[0][lat][lon]=sum( 
                    val_array[time][lat][lon]*(time_bnds[time][1]-time_bnds[time][0]) 
                    for time in range(time_bnd) ) 
                time_bnd_sum=sum(
                    (time_bnds[time][1]-time_bnds[time][0]) for time in range(time_bnd) )
                
            else:
                avgvals[0][lat][lon]=sum( 
                    val_array[time][lat][lon] for time in range(time_bnd) ) / float(time_bnd)

    if do_weighted_avg: 
        for lat in range(lat_bnd):
            for lon in range(lon_bnd):
                avgvals[0][lat][lon]/=time_bnd_sum
        
    nc_compare=nc.Dataset( ('timavgcsh_atmos_LWP_test1979_5y.nc'), 'r') # for checking the averaging i do against the averaging timavg.csh does
    compare_avgvals=nc_compare[var][:]

    print(
        f'avgvals[0][0][0]        = \
        {avgvals[0][0][0]}'
    )
    print(
        f'compare_avgvals[0][0][0]= \
        {compare_avgvals[0][0][0]}'
    )


    print(
        f'avgvals[0][{lat_bnd-1}][{lon_bnd-1}]        =\
        {avgvals[0][lat_bnd-1][lon_bnd-1]}'
    )

    print(
        f'compare_avgvals[0][{lat_bnd-1}][{lon_bnd-1}]=\
        {compare_avgvals[0][lat_bnd-1][lon_bnd-1]}'
    )

    #assert(False)
                

    #avgvals2=[ [ [ ] ] for time in range(1) ] 
    

                                   

    #assert(False)
    #nc_fout = nc.Dataset( './'+outfile, 'w',persist=True)
    #nc_fout.close()

    


    
    return

# must have done something like `module load fre-nctools`
def generate_frenctools_timavg(targdir=None, targfile=None, outfile=None, debugMode=False):
    if debugMode: print("calling generate_frenctools_timavg for file: " + targdir + targfile)
    targpath=targdir+targfile
    targoutpath=outfile

    import subprocess
    subprocess.Popen(['timavg.csh','-r8','-mb','-o',targoutpath, targpath],
                     stdout=subprocess.PIPE,
                     shell=False)

    return

# must be in conda env with pip-installed cdo package (`pip install cdo --user`)
def generate_cdo_timavg(targdir=None, targfile=None, outfile=None, debugMode=False):    
    if debugMode: print("calling generate_cdo_timavg for file: " + targdir + targfile)
    targpath=targdir+targfile
    targoutpath=outfile
    
    from cdo import Cdo
    cdo=Cdo()
    cdo.timavg(input=targpath, output=targoutpath, returnCdf=True)
    
    return

# function that calls a package-specific time-averaging routine
def generate_time_average(pkg=None, targdir=None, targfile=None, outfile=None, debugMode=False):    
    if debugMode: print("calling generate time averages")

    if   pkg == "cdo"            : generate_cdo_timavg(            targdir, targfile, outfile, debugMode )
    elif pkg == "fre-nctools"    : generate_frenctools_timavg(     targdir, targfile, outfile, debugMode )
    elif pkg == "fre-pythontools": generate_frepythontools_timavg( targdir, targfile, outfile, 'LWP', debugMode )
    else                         : print('requested package unknown. exit.')
    
    return

# above, functions, available via python import
# below, main, --> steering, when called like `python generate_time_averages.py`
def main():
    debugMode=True
    
    ## argument parser TO DO
    COMP='atmos'
    #VAR='droplets'
    VAR='LWP'    
    

    targdir='./testfiles/'    
    targfile1=COMP+'.197901-198312.'+VAR+'.nc' 
    targfile2=COMP+'.198401-198812.'+VAR+'.nc'
    
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
    cli_args = argparser.parse_args()
    #print(cli_args.outf)
    #print(cli_args.inf)
    #print('cli_args={cli_args}')
    


    # ---------------------------------------- cdo timavg calls ---------------------------------------- #
    #generate_time_average( 'cdo', targdir, targfile1, 'test_cdo_pypi_1.nc', debugMode)    
    #generate_time_average( 'cdo', targdir, targfile2, 'test_cdo_pypi_2.nc', debugMode)

    # ---------------------------------------- fre-nctools timavg.csh calls ---------------------------------------- #
    #generate_time_average( 'fre-nctools', targdir, targfile1, 'test_frenc_pypi_1.nc', debugMode)    
    #generate_time_average( 'fre-nctools', targdir, targfile2, 'test_frenc_pypi_2.nc', debugMode)

    # ---------------------------------------- fre-python-tools gen time average calls ---------------------------------------- #
    generate_time_average( 'fre-pythontools', targdir, targfile1, 'test_frenc_pypi_1.nc', debugMode)    
    #generate_time_average( 'fre-python-tools', targdir, targfile2, 'test_frenc_pypi_2.nc', debugMode)    

    return
    
if __name__ == "__main__":
    print("calling main()) \n")
    start_time=time.perf_counter()
    main() 
    finish_time=time.perf_counter()
    print("\n done calling main()")
    print(f'Finished in {round(finish_time - start_time , 2)} second(s)')































    
    #sys.exit(main())

############ OLD SNIPPETS I DONT WANNA GET RID OF YET

    #print('peeking at file....')
    #import peekatfiles as pkf
    #pkf.peekatfile('./test_cdo_pypi_1.nc')


    #nc_fin = nc.Dataset(targpath, "r")
        
            #if debugMode:
    #    cdo.debug=True
    #    
    #    print('printing metadata for input file:'+targfile)
    #    md_dict=nc_fin.__dict__
    #    print(md_dict)
    #
    #    print(cdo.sinfov(targdir+targfile))



    #targoutpath=targdir+outfile
    #nc_fout = nc.Dataset( './'+outfile, 'w',persist=True)
    #nc_fout.close()


        #targdir='./'    
    # /archive/Ciheim.Brown/am5/2022.01/c96L33_am5f1a0r0_amip/gfdl.ncrc4-intel21-prod-openmp/pp/atmos/ts/monthly/5yr/
    #targdir ='/archive/Ciheim.Brown/am5/2022.01/c96L33_am5f1a0r0_amip/gfdl.ncrc4-intel21-prod-openmp/pp/atmos/ts/monthly/5yr/'
    #targfile='atmos.197901-198312.LWP.nc'
    #if debugMode: print("calling generate time averages for file: " + targdir + targfile)
    #generate_time_averages(targdir,targfile,'test_cdo_pypi_1.nc',debugMode)
    #targfile='atmos.198401-198812.LWP.nc'
    #if debugMode: print("calling generate time averages for file: " + targdir + targfile)
    #generate_time_averages(targdir,targfile,'test_cdo_pypi_1.nc',debugMode)

