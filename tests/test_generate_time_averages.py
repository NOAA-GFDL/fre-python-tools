import pathlib as pl
time_avg_file_dir=str(pl.Path.cwd())+'/tests/time_avg_test_files/'
test_file_name='atmos.197901-198312.LWP.nc'

def test_time_avg_file_dir_exists():
    ''' look for input test file directory '''
    assert pl.Path(time_avg_file_dir).exists()

def test_time_avg_input_file_exists():
    ''' look for input test file '''
    assert pl.Path( time_avg_file_dir + test_file_name ).exists()


### cdo avgs, unweighted, all/seasonal/monthly ------------------------
def test_monthly_cdo_time_unwgt_avgs():
    ''' generates an unweighted monthly time averaged file using cdo '''
    infile =time_avg_file_dir+test_file_name
    monthly_outfile=time_avg_file_dir+'ymonmean_unwgt_'+test_file_name

    if pl.Path(monthly_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(monthly_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(infile = infile, outfile = monthly_outfile, pkg='cdo', avg_type='month', unwgt=True)
    assert pl.Path(monthly_outfile).exists()

def test_seasonal_cdo_time_unwgt_avgs():
    ''' generates an unweighted seasonal time averaged file using cdo '''
    infile =time_avg_file_dir+test_file_name
    seasonal_outfile=time_avg_file_dir+'yseasmean_unwgt_'+test_file_name

    if pl.Path(seasonal_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(seasonal_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(infile = infile, outfile = seasonal_outfile, pkg='cdo', avg_type='seas', unwgt=True)
    assert pl.Path(seasonal_outfile).exists()

def test_cdo_time_unwgt_avgs():
    ''' generates an unweighted time averaged file using cdo '''
    infile =time_avg_file_dir+test_file_name
    all_outfile=time_avg_file_dir+'timmean_unwgt_'+test_file_name

    if pl.Path(all_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(all_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(infile = infile, outfile = all_outfile, pkg='cdo', avg_type='all', unwgt=True)
    assert pl.Path(all_outfile).exists()


### cdo avgs, weighted, all/seasonal/monthly ------------------------
# TO DO: MAKE THESE
#def test_monthly_cdo_time_avgs():
#def test_seasonal_cdo_time_avgs():

def test_cdo_time_avgs():
    ''' generates a weighted time averaged file using cdo '''
    infile =time_avg_file_dir+test_file_name
    all_outfile=time_avg_file_dir+'timmean_'+test_file_name

    if pl.Path(all_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(all_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(infile = infile, outfile = all_outfile, pkg='cdo', avg_type='all', unwgt=False)
    assert pl.Path(all_outfile).exists()


### cdo stddevs, unweighted, all/seasonal/monthly ------------------------
def test_monthly_cdo_time_unwgt_stddevs():
    ''' generates a monthly time averaged file using cdo '''
    infile =time_avg_file_dir+test_file_name
    monthly_outfile=time_avg_file_dir+'ymonstddev1_unwgt_'+test_file_name

    if pl.Path(monthly_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(monthly_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(infile = infile, outfile = monthly_outfile, pkg='cdo', avg_type='month', stddev_type='samp')
    assert pl.Path(monthly_outfile).exists()

def test_seasonal_cdo_time_unwgt_stddevs():
    ''' generates a seasonal time averaged file using cdo '''
    infile =time_avg_file_dir+test_file_name
    seasonal_outfile=time_avg_file_dir+'yseasstddev1_unwgt_'+test_file_name

    if pl.Path(seasonal_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(seasonal_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(infile = infile, outfile = seasonal_outfile, pkg='cdo', avg_type='seas', stddev_type='samp')
    assert pl.Path(seasonal_outfile).exists()

def test_cdo_time_unwgt_stddevs():
    ''' generates a time averaged file using cdo '''
    infile =time_avg_file_dir+test_file_name
    all_outfile=time_avg_file_dir+'timstddev1_unwgt_'+test_file_name

    if pl.Path(all_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(all_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(infile = infile, outfile = all_outfile, pkg='cdo', avg_type='all', stddev_type='samp')
    assert pl.Path(all_outfile).exists()

### cdo stddevs, weighted, all/seasonal/monthly ------------------------
# TO DO: MAKE THESE

### frepythontools avgs+stddevs, weighted+unweighted, all ------------------------

def test_fre_python_tools_time_avgs():
    ''' generates a time averaged file using fre_python_tools's version '''
    ''' weighted average, no std deviation '''
    infile =time_avg_file_dir+test_file_name
    all_outfile=time_avg_file_dir+'frepytools_timavg_'+test_file_name

    if pl.Path(all_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(all_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(infile = infile, outfile = all_outfile, pkg='fre-python-tools', unwgt=False, avg_type='all')
    assert pl.Path(all_outfile).exists()

def test_fre_python_tools_time_unwgt_avgs():
    ''' generates a time averaged file using fre_python_tools's version '''
    ''' weighted average, no std deviation '''
    infile =time_avg_file_dir+test_file_name
    all_unwgt_outfile=time_avg_file_dir+'frepytools_unwgt_timavg_'+test_file_name

    if pl.Path(all_unwgt_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(all_unwgt_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(infile = infile, outfile = all_unwgt_outfile, pkg='fre-python-tools', unwgt=True, avg_type='all')
    assert pl.Path(all_unwgt_outfile).exists()

def test_fre_python_tools_time_avgs_stddevs():
    ''' generates a time averaged file using fre_python_tools's version '''
    ''' weighted average, no std deviation '''
    infile =time_avg_file_dir+test_file_name
    all_stddev_outfile=time_avg_file_dir+'frepytools_timavg_stddev_'+test_file_name

    if pl.Path(all_stddev_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(all_stddev_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(infile = infile, outfile = all_stddev_outfile, pkg='fre-python-tools', unwgt=False, stddev_type='samp', avg_type='all')
    assert pl.Path(all_stddev_outfile).exists()

def test_fre_python_tools_time_unwgt_avgs_stddevs():
    ''' generates a time averaged file using fre_python_tools's version '''
    ''' weighted average, no std deviation '''
    infile =time_avg_file_dir+test_file_name
    all_unwgt_stddev_outfile=time_avg_file_dir+'frepytools_unwgt_timavg_stddev_'+test_file_name

    if pl.Path(all_unwgt_stddev_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(all_unwgt_stddev_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(infile = infile, outfile = all_unwgt_stddev_outfile, pkg='fre-python-tools', unwgt=True, stddev_type='samp', avg_type='all')
    assert pl.Path(all_unwgt_stddev_outfile).exists()

# TO DO: MAKE THESE
#def test_monthly_fre_python_tools_time_avgs():
#def test_monthly_fre_python_tools_time_unwgt_avgs():
#def test_monthly_fre_python_tools_time_avgs_stddevs():
#def test_monthly_fre_python_tools_time_unwgt_avgs_stddevs():
#
#def test_seasonal_fre_python_tools_time_avgs():
#def test_seasonal_fre_python_tools_time_unwgt_avgs():
#def test_seasonal_fre_python_tools_time_avgs_stddevs():
#def test_seasonal_fre_python_tools_time_unwgt_avgs_stddevs(:)



## this will only work at GFDL. dev convenience only.
#alt_str_fre_nctools_inf='tests/time_avg_test_files/fre_nctools_timavg_CLI_test_r8_b_atmos_LWP_1979_5y.nc'
#def test_fre_nctools_time_avgs():
#    ''' generates a time averaged file using fre_python_tools's version '''
#    ''' weighted average, no std deviation '''
#    infile =time_avg_file_dir+test_file_name
#    all_outfile=time_avg_file_dir+'frenctools_timavg_'+test_file_name
#
#    if pl.Path(all_outfile).exists():
#        print(f'output test file exists. deleting before remaking.')
#        pl.Path(all_outfile).unlink() #delete file so we check that it can be recreated
#
#    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
#    gtas.generate_time_average(infile = infile, outfile = all_outfile, pkg='fre-nctools', unwgt=False, avg_type='all')
#    assert pl.Path(all_outfile).exists()


# Numerics-based tests.
# compare frepytools, cdo time-average output to fre-nctools where possible
var='LWP'
str_fre_nctools_inf=time_avg_file_dir+'frenctools_timavg_'+test_file_name # this is now in the repo
str_fre_pytools_inf=time_avg_file_dir+'frepytools_timavg_'+test_file_name
str_cdo_inf=time_avg_file_dir+'timmean_'+test_file_name
str_unwgt_fre_pytools_inf=time_avg_file_dir+'frepytools_unwgt_timavg_'+test_file_name
str_unwgt_cdo_inf=time_avg_file_dir+'timmean_unwgt_'+test_file_name
def test_compare_fre_python_tools_to_fre_nctools():

    import numpy as np
    import netCDF4 as nc
    fre_pytools_inf=nc.Dataset(str_fre_pytools_inf,'r')

    try:
        fre_nctools_inf=nc.Dataset(str_fre_nctools_inf,'r')
    except:
        print('fre-nctools input file not found. \
        probably because you are not at GFDL! run the shell script \
        example if you would like to see this pass. otherwise, \
        i will error right after this message.')


        try:
            fre_nctools_inf=nc.Dataset(alt_str_fre_nctools_inf,'r')
        except:
            print('fre-nctools output does not exist. create it first!')
            assert False

    fre_pytools_timavg=fre_pytools_inf[var][:].copy()
    fre_nctools_timavg=fre_nctools_inf[var][:].copy()


    assert all([ len(fre_pytools_timavg)==len(fre_nctools_timavg),
                len(fre_pytools_timavg[0])==len(fre_nctools_timavg[0]),
                 len(fre_pytools_timavg[0][0])==len(fre_nctools_timavg[0][0]) ])

    diff_pytools_nctools_timavg=fre_pytools_timavg-fre_nctools_timavg
    #diff_pytools_nctools_timavg=np.moveaxis( diff_pytools_nctools_timavg[:], 0, -1) #move time axis to inner index

    for lat in range(0,len(diff_pytools_nctools_timavg[0])):
        for lon in range(0,len(diff_pytools_nctools_timavg[0][0])):
            print(f'lat={lat},lon={lon}')
            print(f'diff_pytools_nctools_timavg[0][lat][lon]={diff_pytools_nctools_timavg[0][lat][lon]}')
            if lon>10: break
        break
    #print(f'a row of the differences: {diff_pytools_nctools_timavg[0][:]}')
    non_zero_count=np.count_nonzero(diff_pytools_nctools_timavg[:])
    #print(f'non_zero_count=np.count_nonzero(array)={non_zero_count}')
    #print(f'numpy.all(diff array)= {np.all(diff_pytools_nctools_timavg[0][:])}')

    #assert (non_zero_count == 0.) # bad way to check for zero
    #assert not( non_zero_count > 0.) and not(non_zero_count < 0.) # better but i like factoring...
    assert not( (non_zero_count > 0.) or (non_zero_count < 0.) ) # not as readable maybe but equivalent


def test_compare_fre_python_tools_to_cdo():


    import numpy as np
    import netCDF4 as nc
    fre_pytools_inf=nc.Dataset(str_fre_pytools_inf,'r')

    try:
        cdo_inf=nc.Dataset(str_cdo_inf,'r')
    except:
        print('cdo input file not found. run cdo tests first.')
        assert False

    fre_pytools_timavg=fre_pytools_inf[var][:].copy()
    cdo_timavg=cdo_inf[var][:].copy()

    assert all([ len(fre_pytools_timavg)==len(cdo_timavg),
                len(fre_pytools_timavg[0])==len(cdo_timavg[0]),
                 len(fre_pytools_timavg[0][0])==len(cdo_timavg[0][0]) ])

    diff_pytools_cdo_timavg=fre_pytools_timavg-cdo_timavg

    for lat in range(0,len(diff_pytools_cdo_timavg[0])):
        for lon in range(0,len(diff_pytools_cdo_timavg[0][0])):
            print(f'lat={lat},lon={lon}')
            print(f'diff_pytools_cdo_timavg[0][lat][lon]={diff_pytools_cdo_timavg[0][lat][lon]}')
            if lon>10: break
        break

    non_zero_count=np.count_nonzero(diff_pytools_cdo_timavg[:])

    assert not( (non_zero_count > 0.) or (non_zero_count < 0.) ) # not as readable maybe but equivalent


def test_compare_unwgt_fre_python_tools_to_unwgt_cdo():

    import numpy as np
    import netCDF4 as nc
    fre_pytools_inf=nc.Dataset(str_unwgt_fre_pytools_inf,'r')

    try:
        cdo_inf=nc.Dataset(str_unwgt_cdo_inf,'r')
    except:
        print('cdo input file not found. run cdo tests first.')
        assert False

    fre_pytools_timavg=fre_pytools_inf[var][:].copy()
    cdo_timavg=cdo_inf[var][:].copy()

    assert all([ len(fre_pytools_timavg)==len(cdo_timavg),
                len(fre_pytools_timavg[0])==len(cdo_timavg[0]),
                 len(fre_pytools_timavg[0][0])==len(cdo_timavg[0][0]) ])

    diff_pytools_cdo_timavg=fre_pytools_timavg-cdo_timavg

    for lat in range(0,len(diff_pytools_cdo_timavg[0])):
        for lon in range(0,len(diff_pytools_cdo_timavg[0][0])):
            print(f'lat={lat},lon={lon}')
            print(f'diff_pytools_cdo_timavg[0][lat][lon]={diff_pytools_cdo_timavg[0][lat][lon]}')
            if lon>10: break
        break

    non_zero_count=np.count_nonzero(diff_pytools_cdo_timavg[:])

    assert not( (non_zero_count > 0.) or (non_zero_count < 0.) ) # not as readable maybe but equivalent


def test_compare_cdo_to_fre_nctools():

    import numpy as np
    import netCDF4 as nc
    cdo_inf=nc.Dataset(str_cdo_inf,'r')

    try:
        fre_nctools_inf=nc.Dataset(str_fre_nctools_inf,'r')
    except:
        print('fre-nctools input file not found. \
        probably because you are not at GFDL! run the shell script \
        example if you would like to see this pass. otherwise, \
        i will error right after this message.')
        alt_str_fre_nctools_inf='tests/time_avg_test_files/fre_nctools_timavg_CLI_test_r8_b_atmos_LWP_1979_5y.nc'

        try:
            fre_nctools_inf=nc.Dataset(alt_str_fre_nctools_inf,'r')
        except:
            print('fre-nctools output does not exist. create it first!')
            assert False

    cdo_timavg=cdo_inf[var][:].copy()
    fre_nctools_timavg=fre_nctools_inf[var][:].copy()


    assert all([ len(cdo_timavg)==len(fre_nctools_timavg),
                len(cdo_timavg[0])==len(fre_nctools_timavg[0]),
                 len(cdo_timavg[0][0])==len(fre_nctools_timavg[0][0]) ])

    diff_cdo_nctools_timavg=cdo_timavg-fre_nctools_timavg

    for lat in range(0,len(diff_cdo_nctools_timavg[0])):
        for lon in range(0,len(diff_cdo_nctools_timavg[0][0])):
            print(f'lat={lat},lon={lon}')
            print(f'diff_cdo_nctools_timavg[0][lat][lon]={diff_cdo_nctools_timavg[0][lat][lon]}')
            if lon>10: break
        break

    non_zero_count=np.count_nonzero(diff_cdo_nctools_timavg[:])

    assert not( (non_zero_count > 0.) or (non_zero_count < 0.) ) # not as readable maybe but equivalent
