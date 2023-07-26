''' class for python-native routine usuing netCDF4 and numpy to crunch time-averages '''
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

        if self.avg_type != 'all':
            print(f'ERROR: avg_type={self.avg_type} not supported at this time.')
            return 1

        import math
        import numpy
        from netCDF4 import Dataset

        nc_fin = Dataset(infile, 'r')
        if nc_fin.file_format != 'NETCDF4':
            print(f'INFO: input file is not netCDF4 format, is {nc_fin.file_format}')


        #identifying the input variable to computer statistics should involve one of two things:
        # user input specifying to exact variable to target OR
        # a separate routine that attempts to intelligently identify the target variable.
        if self.var is not None:
            targ_var = self.var
        else:
            targ_var = infile.split('/').pop().split('.')[-2]
        
        if __debug__:
            print(f'targ_var={targ_var}')


        # check for the variable we're hoping is in the file
        nc_fin_vars = nc_fin.variables
        for key in nc_fin_vars:
            if str(key) == targ_var:
                time_bnds = nc_fin['time_bnds'][:].copy()
                key_found = True
                break
        if not key_found:
            print('requested variable not found. exit.')
            return 1


        # check for mask, adjust accordingly TO DO
        #is_masked = ma.is_masked(val_array)

        # read in sizes of specific axes / compute weights
        # weights can be encoded as a class member, whose existence
        # depends on the user specifying unwgt=True, if vect_wgts=None, set the avg
        # and stddev gen functions to the appropriate behavior TO DO
        fin_dims = nc_fin.dimensions
        num_time_bnds = fin_dims['time'].size
        if not self.unwgt: #compute sum of weights
            wgts = numpy.moveaxis( time_bnds,0,-1)[1][:].copy() - numpy.moveaxis( time_bnds,0,-1)[0][:].copy()
            wgts_sum=sum(wgts)
            if __debug__:
                print(f'wgts_sum={wgts_sum}')


        # initialize arrays
        num_lat_bnds=fin_dims['lat'].size
        print(f'num_lat_bnds={num_lat_bnds}')
        num_lon_bnds=fin_dims['lon'].size
        print(f'num_lon_bnds={num_lon_bnds}')
        avgvals=numpy.zeros((1,num_lat_bnds,num_lon_bnds),dtype=float)
        if self.stddev_type is not None:
            print('computing std. deviations')
            stddevs=numpy.zeros((1,num_lat_bnds,num_lon_bnds),dtype=float)

        # this loop behavior 100% should be re-factored into generator functions.
        # they should be slightly faster, and much more readable. TO DO
        # the average/stddev cpu settings should also be genfunctions, their behavior
        # (e.g. stddev_pop v stddev_samp) should be set given user inputs. TO DO
        # the computations can lean on numpy.stat more- i imagine it's faster TO DO
        # parallelism via a module like dask should come after the above improvements TO DO
        if True: #doing this to test metadata writing stuff quicker
            # compute average, for each lat/lon coordinate over time record in file
            if not self.unwgt: #weighted case
                print('computing weighted statistics')
                for lat in range(num_lat_bnds):
                    lon_val_array=numpy.moveaxis( nc_fin[targ_var][:],0,-1)[lat].copy()

                    for lon in range(num_lon_bnds):
                        tim_val_array= lon_val_array[lon].copy()
                        avgvals[0][lat][lon]=sum( (tim_val_array[tim] * wgts[tim] )
                                                  for tim in range(num_time_bnds) ) / wgts_sum

                        if self.stddev_type is not None: # implement stddeviation types TO DO
                            stddevs[0][lat][lon]=math.sqrt(
                                                 sum( wgts[tim] *
                                                      (tim_val_array[tim]-avgvals[0][lat][lon]) ** 2
                                                      for tim in range(num_time_bnds) )
                                                  / wgts_sum )
                        del tim_val_array
                    del lon_val_array
            else: #unweighted case
                print('computing unweighted statistics')
                for lat in range(num_lat_bnds):
                    lon_val_array=numpy.moveaxis( nc_fin[targ_var][:],0,-1)[lat].copy()

                    for lon in range(num_lon_bnds):
                        tim_val_array= lon_val_array[lon].copy()
                        avgvals[0][lat][lon]=sum( # no time sum needed here, b.c. unweighted, so sum
                            tim_val_array[tim] for tim in range(num_time_bnds)
                                   ) / num_time_bnds

                        if self.stddev_type is not None:

                            stddevs[0][lat][lon]=math.sqrt(
                                                          sum(
                                                      (tim_val_array[tim]-avgvals[0][lat][lon]) ** 2
                                                              for tim in range(num_time_bnds)
                                                          ) / ( (num_time_bnds - 1. ) )
                                                               )
                        del tim_val_array
                    del lon_val_array



        # write output file
        # the first pass at this is mediocre
        # i think this is also a class function
        # sep out and work with elsewhere TO DO
        # tests for these functions? TO DO
        #with Dataset( outfile, 'w', format='NETCDF4', persist=True ) as nc_fout:
        #nc_fout= Dataset( outfile, 'w', format='NETCDF4', persist=True )
        nc_fout= Dataset( outfile, 'w', format=nc_fin.file_format, persist=True )

        # write file global attributes
        print('------- writing output attributes. --------')
        #fin_ncattrs=nc_fin.ncattrs()
        unwritten_ncattr_list=[]
        try:
            nc_fout.setncatts(nc_fin.__dict__) #this copies the global attributes exactly.
        except:
            print('could not copy ncatts from input file. trying to copy one-by-one')
            fin_ncattrs=nc_fin.ncattrs()
            for ncattr in fin_ncattrs:
                print(f'\n_________\nncattr={ncattr}')
                try:
                    nc_fout.setncattr(ncattr, nc_fin.getncattr(ncattr))
                except:
                    print(f'could not get nc file attribute: {ncattr}. moving on.')
                    unwritten_ncattr_list.append(ncattr)
        if len(unwritten_ncattr_list)>0:
            print(f'WARNING: unwritten_ncattr_list={unwritten_ncattr_list}')
        print('------- DONE writing output attributes. --------')


        # write file dimensions
        print('\n ------ writing output dimensions. ------ ')
        unwritten_dims_list=[]
        for key in fin_dims:
            try:
                if key=='time':
                    #nc_fout.createDimension( dimname=key, size=None )
                    nc_fout.createDimension( dimname=key, size=1)
                else:
                    nc_fout.createDimension( dimname=key, size=fin_dims[key].size )
            except:
                print(f'problem. cannot read/write dimension {key}')
                unwritten_dims_list.append(key)
        if len(unwritten_dims_list)>0:
            print(f'WARNING: unwritten_dims_list={unwritten_dims_list}')
        print('------ DONE writing output dimensions. ------- \n')
        ##

        
        # first write the data we care most about- those we computed.
        nc_fout.createVariable(targ_var, nc_fin[targ_var].dtype, nc_fin[targ_var].dimensions)
        nc_fout.variables[targ_var].setncatts(nc_fin[targ_var].__dict__) # copying metadata, not fully correct 
                                                                         # but not far from wrong according to CF
                                                                         # cell_methods must be changed TO DO
        nc_fout.variables[targ_var][:]=avgvals
        if self.stddev_type is not None:
            stddev_varname=targ_var+'_'+self.stddev_type+'_stddev'
            nc_fout.createVariable(stddev_varname, nc_fin[targ_var].dtype, nc_fin[targ_var].dimensions)
            nc_fout.variables[stddev_varname].setncatts(nc_fin[targ_var].__dict__)
            nc_fout.variables[stddev_varname][:]=stddevs
        ##    

        # write OTHER output variables (aka data) #prev code.
        print('\n------- writing other output variables. -------- ')
        unwritten_var_list=[]
        unwritten_var_ncattr_dict={}
        for var in nc_fin_vars:
            if var != targ_var:
                print(f'\nattempting to create output variable: {var}')
                #print(f'is it a time variable? {self.var_is_time(nc_fin.variables[var])}')
                nc_fout.createVariable(var, nc_fin[var].dtype, nc_fin[var].dimensions)
                nc_fout.variables[var].setncatts(nc_fin[var].__dict__)
                try:
                    nc_fout.variables[var][:] = nc_fin[var][:]
                except:
                    print(f'could not write var={var}. i bet its the shape!')
                    print(f'nc_fin[var].shape={nc_fin[var].shape}')
                    #print(f'len(nc_fout.variables[{var}])={len(nc_fout.variables[var])}')
                    nc_fout.variables[var][:] = [ nc_fin[var][0] ]
                    print(f'is it a time variable? {self.var_has_time_units(nc_fin.variables[var])}')
            else:
                continue



        if len(unwritten_var_list)>0:
            print(f'WARNING: unwritten_var_list={unwritten_var_list}')
        print(f'unwritten_var_ncattr_dict={unwritten_var_ncattr_dict}')
        print('---------- DONE writing output variables. ---------')
        ##


        nc_fout.close()
        #close input file
        nc_fin.close()
        print(f'wrote ouput file: {outfile}')

        return 0
