import pathlib as pl
time_avg_file_dir=str(pl.Path.cwd())+'/tests/time_avg_test_files/'


def test_time_avg_file_dir_exists():
    ''' look for input test file directory '''
    assert pl.Path(time_avg_file_dir).exists()


def test_time_avg_input_file_exists():
    ''' look for input test file '''
    assert pl.Path( time_avg_file_dir + 'atmos.197901-198312.LWP.nc' ).exists() 


def test_monthly_python_cdo_time_averages():
    ''' generates a monthly time averaged file using cdo '''
    infile =time_avg_file_dir+'atmos.197901-198312.LWP.nc'
    monthly_outfile=time_avg_file_dir+'ymonmean_atmos.197901-198312.LWP.nc'
    
    if pl.Path(monthly_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(monthly_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(pkg='cdo', infile=infile, outfile=monthly_outfile, avg_type='month')
    assert pl.Path(monthly_outfile).exists()


def test_seasonal_python_cdo_time_averages():
    ''' generates a seasonal time averaged file using cdo '''
    infile =time_avg_file_dir+'atmos.197901-198312.LWP.nc'
    seasonal_outfile=time_avg_file_dir+'yseasmean_atmos.197901-198312.LWP.nc'

    if pl.Path(seasonal_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(seasonal_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(pkg='cdo', infile=infile, outfile=seasonal_outfile, avg_type='seas')
    assert pl.Path(seasonal_outfile).exists()


def test_python_cdo_time_averages():
    ''' generates a time averaged file using cdo '''
    infile =time_avg_file_dir+'atmos.197901-198312.LWP.nc'
    all_outfile=time_avg_file_dir+'timmean_atmos.197901-198312.LWP.nc'

    if pl.Path(all_outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(all_outfile).unlink() #delete file so we check that it can be recreated

    from fre_python_tools.generate_time_averages import generate_time_averages as gtas
    gtas.generate_time_average(pkg='cdo', infile=infile, outfile=all_outfile, avg_type='all')
    assert pl.Path(all_outfile).exists()
