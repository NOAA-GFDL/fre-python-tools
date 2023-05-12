#from fre_python_tools.generate_time_averages import *
import pathlib as pl

time_avg_dir=str(pl.Path.cwd())+'/tests/time_avg_test_files/'

def test_cwd_for_tests():
    cwd_path=str( pl.Path.cwd() ).split('/')
    assert (cwd_path.pop() == 'fre-python-tools')

def test_time_avg_file_dir_exists():
    assert pl.Path(time_avg_dir).exists()

def test_time_avg_input_file_exists():
    assert all([ pl.Path( time_avg_dir + 'atmos.197901-198312.LWP.nc' ).exists() ,
                 pl.Path( time_avg_dir + 'atmos.198401-198812.LWP.nc' ).exists() ])    

def test_CLI_time_avg_ex_exists():
    assert all([ pl.Path( './tests/timavgs_CLI_examples.sh'     ).exists() ,
                 pl.Path( './tests/run_timavgs_CLI_examples.sh' ).exists() ])

### OK so calling this bash script from the command line doesn't quite work the way i expected.
### skipping for now.
## this might be what we call a "smolder" test.
## i.e., if it finishes instead of crashing and burning, we're good.
## but if it crashes and burns... we'll figure that out in the next
## test by making sure the output exists
## this is not my favorite test structure.
#def test_CLI_gen_time_avg():
#    from subprocess import Popen, PIPE
#
#    # the script call here itself will remove previously run test output if it
#    # already exists. we want to make sure the files can be recreated
#    run_CLI_time_avgs_cmd=['./tests/run_timavgs_CLI_examples.sh']
#    #run_CLI_time_avgs_cmd=['source', './tests/run_timavgs_CLI_examples.sh']
#    return_code=-1 #this should get assigned None.
#    with Popen(run_CLI_time_avgs_cmd,
#               stdout=PIPE, stderr=PIPE, shell=True) as subp:        
#        print(f'returncode={subp.returncode}')
#        return_code=subp.returncode
#    assert return_code == None

def test_CLI_cdo_time_avg_output_exists():
    assert all([ pl.Path( time_avg_dir+'cdo_ymonmean_CLI_test_atmos_LWP_1979_5y.nc'  ).exists() ,
                 pl.Path( time_avg_dir+'cdo_yseasmean_CLI_test_atmos_LWP_1979_5y.nc' ).exists() ,
                 pl.Path( time_avg_dir+'cdo_timmean_CLI_test_atmos_LWP_1979_5y.nc'   ).exists()   ])
    
def test_cdo_monthly_time_average():
    ''' generates a monthly time averaged file using cdo '''
    from fre_python_tools.generate_time_averages import generate_time_averages as gtas

    infile =time_avg_dir+'atmos.197901-198312.LWP.nc'
    outfile=time_avg_dir+'ymonmean_atmos.197901-198312.LWP.nc'
    print(f' time_avg_dir={time_avg_dir}\n, infile={infile}\n outfile={outfile}\n')
    if pl.Path(outfile).exists():
        print(f'output test file exists. deleting before remaking.')
        pl.Path(outfile).unlink() #delete file so we can check that it can be recreated
        
    #gtas.generate_time_average(pkg='cdo', infile=infile, outfile=outfile, avg_type='month')
    #gtas.generate_time_average(pkg='cdo', infile=infile, outfile=outfile, avg_type='seas')
    gtas.generate_time_average(pkg='cdo', infile=infile, outfile=outfile, avg_type='all')
    #gta.generate_time_average(pkg='cdo', infile=infile, outfile=outfile, avg_type='monthly')
    assert pl.Path(outfile).exists()

#def test_frepytools_time_averages():
#    ''' doc string '''
#    print(f'HELLO WORLD from test_frepytools_time_averages')
#    assert True
