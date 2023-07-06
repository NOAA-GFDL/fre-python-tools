from .timeAverager import timeAverager

class frepytoolsTimeAverager(timeAverager):
    '''
    class inheriting from abstract base class timeAverager
    generates time-averages using a python-native approach
    avoids using other third party statistics functions by design.
    '''


    def generate_timavg(self, infile=None, outfile=None):
        ''' my own time-averaging function. mostly an exercise. '''
        if __debug__:
            print('calling generate_frepythontools_timavg for file: ' + infile)
            
        if avg_type!='all':
            print(f'ERROR: avg_type={avg_type} is not supported by this function at this time.')
            return 1

        import math
        import numpy
        from netCDF4 import Dataset
    
        nc_fin = Dataset(infile, 'r')
        
        nc_fin_var=infile.split('/').pop().split('.')[-2]
        if __debug__:
            print(f'nc_fin_var={nc_fin_var}')
            

        # check for the variable we're hoping is in the file
        fin_vars=nc_fin.variables
        for key in fin_vars:
            if str(key)==nc_fin_var:
                time_bnds=nc_fin['time_bnds'][:].copy()
                key_found=True
                break
        if not key_found:
            print('requested variable not found. exit.')
            return 1
       

        # check for mask, adjust accordingly TO DO
        #is_masked = ma.is_masked(val_array)

        # read in sizes of specific axes
        fin_dims =nc_fin.dimensions
        N_time_bnds=fin_dims['time'].size
        if not unwgt: #compute sum of weights
            wgts=numpy.moveaxis(time_bnds,0,-1)[1][:].copy() - numpy.moveaxis(time_bnds,0,-1)[0][:].copy()
            wgts_sum=sum(wgts)
            if __debug__:
                print(f'wgts_sum={wgts_sum}')


        # initialize arrays
        lat_bnd=fin_dims['lat'].size
        print(f'lat_bnd={lat_bnd}')
        lon_bnd=fin_dims['lon'].size
        print(f'lon_bnd={lon_bnd}')
        avgvals=numpy.zeros((1,lat_bnd,lon_bnd),dtype=float)
        if stddev:
            print(f'computing std. deviations')
            stddevs=numpy.zeros((1,lat_bnd,lon_bnd),dtype=float)

        # compute average, for each lat/lon coordinate over time record in file
        if not unwgt: #weighted case
            print(f'computing weighted statistics')
            for lat in range(lat_bnd):
                lon_val_array=numpy.moveaxis( nc_fin[nc_fin_var][:],0,-1)[lat].copy()
            
                for lon in range(lon_bnd):
                    tim_val_array= lon_val_array[lon].copy() 
                    avgvals[0][lat][lon]=sum( (tim_val_array[tim] * wgts[tim] )
                                              for tim in range(N_time_bnds) ) / wgts_sum

                    if stddev: # use sample and/or estimated pop std. dev. 
                        stddevs[0][lat][lon]=math.sqrt(
                                                 sum( wgts[tim] *
                                                      (tim_val_array[tim]-avgvals[0][lat][lon]) ** 2.
                                                      for tim in range(N_time_bnds) )
                                                  / wgts_sum )
                    del tim_val_array
                del lon_val_array
        else: #unweighted case
            print(f'computing unweighted statistics')
            for lat in range(lat_bnd):
                lon_val_array=numpy.moveaxis( nc_fin[nc_fin_var][:],0,-1)[lat].copy()
                
                for lon in range(lon_bnd):
                    tim_val_array= lon_val_array[lon].copy() 
                    avgvals[0][lat][lon]=sum( # no time sum needed here, b.c. unweighted, so sum
                        tim_val_array[tim] for tim in range(N_time_bnds)
                                   ) / N_time_bnds

                    if stddev:
                    
                        stddevs[0][lat][lon]=math.sqrt(
                                                          sum(
                                                              (tim_val_array[tim]-avgvals[0][lat][lon]) ** 2.
                                                              for tim in range(N_time_bnds)
                                                          ) / ( (N_time_bnds - 1. ) )
                                                               )
                    del tim_val_array
                del lon_val_array

        # write output file
        #with Dataset( outfile, 'w', format='NETCDF4', persist=True ) as nc_fout:
        nc_fout= Dataset( outfile, 'w', format='NETCDF4', persist=True )
        
        # write file dimensions
        print('\nwriting output dimensions.')
        for key in fin_dims:
            #print(f'key={key}')
            if key=='time':
                try:
                    nc_fout.createDimension( dimname='time', size=1 )
                except:
                    print(f'problem. cannot read/write time dimensions')
                    return 1        
            else:            
                nc_fout.createDimension( dimname=key, size=fin_dims[key].size )
        print('done writing output dimensions.\n')
        ##
        
        # write output variables (aka data)
        print('\nwriting output variables.')
        unwritten_var_list=[]
        for var in fin_vars:
            print(f'\nattempting to create output variable: {var}')    #nc_fout.createVariable(var, fin_vars[var].dtype, (var))
            try:
                nc_fout.createVariable(var, fin_vars[var].dtype, fin_vars[var].dimensions)
                if var ==nc_fin_var:#our averaged variable
                    nc_fout.variables[var][:]=avgvals
                    if stddev:
                        nc_fout.createVariable(var+'_stddevmean', fin_vars[var].dtype, fin_vars[var].dimensions)
                        nc_fout.variables[var+'_stddevmean'][:]=stddevs
                print(f'\nlooking at attributes of variable: {var}')
                for ncattr in fin_vars[var].ncattrs():
                    print(f'ncattr={ncattr}')
                    try: nc_fout.variables[var].setncattr(ncattr, fin_vars[var].getncattr(ncattr))
                    except: print(f'could not read var={var} ncattr={ncattr}')
            except:
                unwritten_var_list.append(var)
                print(f'WARNING: could not create output variable: {var}')
                print(f'____________________________________________________________________________')
                print(f'var={var}')
                print(f'fin_vars[{var}].dtype={fin_vars[var].dtype}')
                print(f'fin_vars[{var}]={fin_vars[var]}')
                print(f'fin_vars[{var}].dimensions={fin_vars[var].dimensions}')
                print(f'          ------------------------------------------------------------      ')
        print('done writing output variables.')
        ##



        # write file global attributes
        print('writing output attributes.')
        fin_ncattrs=nc_fin.ncattrs()
        unwritten_ncattr_list=[]
        for ncattr in fin_ncattrs:
            print(f'\n_________\nncattr={ncattr}')
            try:
                print(f'{repr(fin_ncattrs.getncattr(ncattr))}')
            except:
                print(f'could not get nc file attribute: {ncattr}')
                unwritten_ncattr_list.append(ncattr)
        #    if key=='time':
        #        nc_fout.createVariable( dimname='time', size=1 )
        #    else:
        #        nc_fout.createVariable( dimname=key, size=fin_dims[key].size)            
        
    


        nc_fout.close()
        #close input file
        nc_fin.close()
        print(f'wrote ouput file: {outfile}')
        if len(unwritten_var_list)>0:
            print(f'WARNING: unwritten_var_list={unwritten_var_list}')
        if len(unwritten_ncattr_list)>0:
            print(f'WARNING: unwritten_ncattr_list={unwritten_ncattr_list}')
            
        return 0



