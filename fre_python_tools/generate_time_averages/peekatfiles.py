import os, sys
import time as tm
import numpy, json
import netCDF4 as nc
import string
from shutil import copyfile

##not working
#def walktree(top):
#    print('walktree call')
#    print('top={top}')
#    print(top.groups.values())
#    #yield top.groups.values()
#    for value in top.groups.values():
#        yield from walktree(value)
#
##not working            
#def peekatfile_walk(fname=None):
#    print('peekatfile_walk call')
#
#    # snipped this from https://github.com/Unidata/netcdf4-python/blob/master/examples/tutorial.py
#    f = nc.Dataset(fname, 'a')
#    
#    print(f.groups)
#
#    print('about to print children')
#    for children in walktree(f):
#        for child in children:
#            print(child)
#
#    return
        
def peekatfile(fname=None, printVals=False):
    
    # to use, `python peekatfiles.py`
    #fname='test.nc'
    #f = nc.Dataset(fname, "r", "NETCDF4")
    f = nc.Dataset(fname)
    
    
    print ('printing netCDF4 file summary of file'+fname)
    print ('\n')
    
    
    # print root group? of the netCDF4 file
    print ('---------------- print(f) ----------------------')
    print(f)
    print ('\n')
    
    
    md=f.__dict__
    print ('---------------- print metadata dict ----------------------')
    print('type(md)='+str(type(md)))
    
    ##whole dict
    #print(md)
    
    for key in md:
        print('md['+str(key)+']='+str(md[key]))
        print ('\n')
        
        
        
    dims_dict=f.dimensions
    print ('---------------- print dimensions + values ----------------------')
    #print('type(f.dimensions.values())='+str(type(f.dimensions.values())))
    print('\n')
    for key in dims_dict:
        print('dims_dict[{key}]=\n   {dims_dict[key]}')
        #print('dims_dict['+str(key)+']=\n'+str(dims_dict[key]))
        print('\n')
    print('\n')
        
    #print('type(f.dimensions.values())='+str(type(f.dimensions.values())))
    #print('\n')
    #for dim in f.dimensions.values():
    #    #print('f.dimensions.values()['+str(dim)+']')
    #    print(dim)
    #print ('\n')

    
    var_dict=f.variables
    print ('---------------- print variables + values ----------------------')
    print('\n')
    for key in var_dict:
        print('var_dict['+str(key)+']=\n'+str(var_dict[key]))
        print('\n')
        if (str(key)=='LWP') and (printVals):
            valarray=f[key][:]
            print('type(valarray)='+str(type(valarray)))
            print(valarray)
            print('--------------------------------')
            for i in range(0,len(valarray)):
                print('valarray['+str(i)+']='+str(valarray[i]))
            #break
    print ('\n')
    #return
    #print('type(f.variables.values())='+str(type(f.variables.values())))
    #print('\n')
    #for var in f.variables.values():
    #    #print('f.variables.values()['+str(var)+']')
    #    print(var)
    #    print('\n')
    #print ('\n')

    return



def main(outfname=None):
    #print('outfname='+str(outfname))
    #return
    indir='./testfiles/'
    fname1='atmos.197901-198312.LWP.nc'
    infile1=indir+fname1
    fname2='atmos.198401-198812.LWP.nc'
    infile2=indir+fname2

    #print('peeking at file ')
    #peekatfile('/archive/Ciheim.Brown/am5/2022.01/c96L33_am5f1a0r0_amip/gfdl.ncrc4-intel21-prod-openmp/pp/atmos/ts/monthly/5yr/atmos.197901-198312.LWP.nc')    

    #print('peeking at file ')
    #peekatfile('/archive/Ciheim.Brown/am5/2022.01/c96L33_am5f1a0r0_amip/gfdl.ncrc4-intel21-prod-openmp/pp/atmos/ts/monthly/5yr/atmos.198401-198812.LWP.nc')

    #print('peeking at file ./test.nc')
    #peekatfile('./3test.nc')
    #peekatfile('./cdo_test.nc')
    
    
    #import subprocess
    # doesn't work, don't need it. 
    # having fre-nctools loaded before calling script is sufficient
    #output=subprocess.Popen(["module","load","fre-nctools"], subprocess.PIPE) 
    
    # this does work, i get timavg.csh's helpmenu back this way.
    #output=subprocess.Popen(["timavg.csh"], stdout=subprocess.PIPE)
    #print((output.communicate()[0]).decode())
    #peekatfile(infile1)

    # does not work.
    #peekatfile_walk(infile1)
    
    print('done peeking at stuff')
    return


if __name__=="__main__":
    main()




