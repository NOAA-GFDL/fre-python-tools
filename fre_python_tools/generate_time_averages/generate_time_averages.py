#!/usr/bin/env python
#import argparse
#import os, sys
import netCDF4 as nc
import time

# within one's conda / python env
# need to `pip install cdo (--user)`
from cdo import Cdo


def generate_time_averages(targdir=None, targfile=None, outfile=None, debugMode=False):
    targpath=targdir+targfile
    #nc_fin = nc.Dataset(targpath, "r")
    cdo=Cdo()

    #if debugMode:
    #    cdo.debug=True
    #    
    #    print('printing metadata for input file:'+targfile)
    #    md_dict=nc_fin.__dict__
    #    print(md_dict)
    #
    #    print(cdo.sinfov(targdir+targfile))

    targoutpath=targdir+outfile
    #nc_fout = nc.Dataset( './'+outfile, 'w',persist=True)
    0cdo.timavg(input=targpath, output=targoutpath,options='-f nc', returnCdf=True)
    #print(stuff)
    #nc_fout.close()
    
    return

def main():
    debugMode=True
    
    ## argument parser TO DO
    #parser = argparse.ArgumentParser(description="generate time averages for specified set of netCDF files. Example: \
    #generate-time-averages.py /path/to/your/files/")
    #parser.add_argument('-h', '--help',
    #                    help="display help summary of options and usage examples.")    
    #args = parser.parse_args()

    #targdir='./'    
    #targdir ='/archive/Ciheim.Brown/am5/2022.01/c96L33_am5f1a0r0_amip/gfdl.ncrc4-intel21-prod-openmp/pp/atmos/ts/monthly/5yr/'
    #targfile='atmos.197901-198312.LWP.nc'
    #if debugMode: print("calling generate time averages for file: " + targdir + targfile)
    #generate_time_averages(targdir,targfile,'test_cdo_pypi_1.nc',debugMode)
    #targfile='atmos.198401-198812.LWP.nc'
    #if debugMode: print("calling generate time averages for file: " + targdir + targfile)
    #generate_time_averages(targdir,targfile,'test_cdo_pypi_1.nc',debugMode)

    targdir='./'    
    #targdir ='/archive/Ciheim.Brown/am5/2022.01/c96L33_am5f1a0r0_amip/gfdl.ncrc4-intel21-prod-openmp/pp/atmos/ts/monthly/5yr/'
    targfile='atmos.197901-198312.droplets.nc'
    if debugMode: print("calling generate time averages for file: " + targdir + targfile)
    generate_time_averages(targdir,targfile,'test_cdo_pypi_1.nc',debugMode)    
    
    #if debugMode: print("done with analyze_gcplog")

    return
    
if __name__ == "__main__":
    start_time=time.perf_counter()
    print("calling main()) \n")
    #sys.exit(main())
    main()
    print("\n done. calling main()")
    finish_time=time.perf_counter()
    print(f'Finished in {round(finish_time - start_time , 2)} second(s)')

    print('peeking at file....')
    import peekatfiles as pkf
    pkf.peekatfile('./test_cdo_pypi_1.nc')
