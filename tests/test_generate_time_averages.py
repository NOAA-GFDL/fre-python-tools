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
    gtas.generate_time_average(pkg='cdo', infile=infile, outfile=monthly_outfile, avg_type='month', unwgt=True)
    assert pl.Path(monthly_outfile).exists()

def test_seasonal_cdo_time_unwgt_avgs():
    ''' generates an unweighted seasonal time averaged file using cdo '''
    infile =time_avg_file_dir+test_file_name
    seasonal_outfile=time_avg_file_dir+'yseasmean_unwgt_'+test_file_name

    if pl.Path(seasonal_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(seasonal_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(pkg='cdo', infile=infile, outfile=seasonal_outfile, avg_type='seas', unwgt=True)
    assert pl.Path(seasonal_outfile).exists()

def test_cdo_time_unwgt_avgs():
    ''' generates an unweighted time averaged file using cdo '''
    infile =time_avg_file_dir+test_file_name
    all_outfile=time_avg_file_dir+'timmean_unwgt_'+test_file_name

    if pl.Path(all_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(all_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(pkg='cdo', infile=infile, outfile=all_outfile, avg_type='all', unwgt=True)
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
    gtas.generate_time_average(pkg='cdo', infile=infile, outfile=all_outfile, avg_type='all', unwgt=False)
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
    gtas.generate_time_average(pkg='cdo', infile=infile, outfile=monthly_outfile, avg_type='month', stddev=True)
    assert pl.Path(monthly_outfile).exists()

def test_seasonal_cdo_time_unwgt_stddevs():
    ''' generates a seasonal time averaged file using cdo '''
    infile =time_avg_file_dir+test_file_name
    seasonal_outfile=time_avg_file_dir+'yseasstddev1_unwgt_'+test_file_name

    if pl.Path(seasonal_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(seasonal_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(pkg='cdo', infile=infile, outfile=seasonal_outfile, avg_type='seas', stddev=True)
    assert pl.Path(seasonal_outfile).exists()

def test_cdo_time_unwgt_stddevs():
    ''' generates a time averaged file using cdo '''
    infile =time_avg_file_dir+test_file_name
    all_outfile=time_avg_file_dir+'timstddev1_unwgt_'+test_file_name

    if pl.Path(all_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(all_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(pkg='cdo', infile=infile, outfile=all_outfile, avg_type='all', stddev=True)
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
    gtas.generate_time_average(pkg='fre-python-tools', infile=infile, outfile=all_outfile, unwgt=False, stddev=False, avg_type='all')
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
    gtas.generate_time_average(pkg='fre-python-tools', infile=infile, outfile=all_unwgt_outfile, unwgt=True, stddev=False, avg_type='all')
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
    gtas.generate_time_average(pkg='fre-python-tools', infile=infile, outfile=all_stddev_outfile, unwgt=False, stddev=True, avg_type='all')
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
    gtas.generate_time_average(pkg='fre-python-tools', infile=infile, outfile=all_unwgt_stddev_outfile, unwgt=True, stddev=True, avg_type='all')
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
