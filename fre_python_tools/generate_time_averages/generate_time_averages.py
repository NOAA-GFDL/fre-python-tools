#!/usr/bin/env python

#import argparse
import time
#import os, sys
#import netCDF4 as nc

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

    if   pkg == "cdo"        : generate_cdo_timavg(targdir, targfile, outfile, debugMode)
    elif pkg == "fre-nctools": generate_frenctools_timavg(targdir, targfile, outfile, debugMode)
    else                     : print('requested package unknown. exit.')
    
    return

# above, functions, available via python import
# below, main, --> steering, when called like `python generate_time_averages.py`
def main():
    debugMode=True
    
    ## argument parser TO DO
    COMP='atmos'
    VAR='droplets'    
    
    # /archive/Ciheim.Brown/am5/2022.01/c96L33_am5f1a0r0_amip/gfdl.ncrc4-intel21-prod-openmp/pp/atmos/ts/monthly/5yr/
    targdir='./testfiles/'    
    targfile1=COMP+'.197901-198312.'+VAR+'.nc' 
    targfile2=COMP+'.198401-198812.'+VAR+'.nc'

    #parser = argparse.ArgumentParser(description="generate time averages for specified set of netCDF files. Example: \
    #generate-time-averages.py /path/to/your/files/")
    #parser.add_argument('-h', '--help',
    #                    help="display help summary of options and usage examples.")    
    #args = parser.parse_args()

    # ---------------------------------------- cdo timavg calls ---------------------------------------- #
    generate_time_average( 'cdo', targdir, targfile1, 'test_cdo_pypi_1.nc', debugMode)    
    #generate_time_average( 'cdo', targdir, targfile2, 'test_cdo_pypi_2.nc', debugMode)

    # ---------------------------------------- fre-nctools timavg.csh calls ---------------------------------------- #
    #generate_time_average( 'fre-nctools', targdir, targfile1, 'test_frenc_pypi_1.nc', debugMode)    
    #generate_time_average( 'fre-nctools', targdir, targfile2, 'test_frenc_pypi_2.nc', debugMode)    

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
    #targdir ='/archive/Ciheim.Brown/am5/2022.01/c96L33_am5f1a0r0_amip/gfdl.ncrc4-intel21-prod-openmp/pp/atmos/ts/monthly/5yr/'
    #targfile='atmos.197901-198312.LWP.nc'
    #if debugMode: print("calling generate time averages for file: " + targdir + targfile)
    #generate_time_averages(targdir,targfile,'test_cdo_pypi_1.nc',debugMode)
    #targfile='atmos.198401-198812.LWP.nc'
    #if debugMode: print("calling generate time averages for file: " + targdir + targfile)
    #generate_time_averages(targdir,targfile,'test_cdo_pypi_1.nc',debugMode)

