#!/usr/bin/env python
''' tools for generating time averages from various packages '''
import argparse

def generate_time_average(infile=None, outfile=None,
                          pkg=None, var=None,
                          unwgt=False, avg_type=None, stddev_type=None):
    ''' steering function to various averaging functions above'''
    if __debug__:
        print(locals()) #input argument details
    exitstatus=1

    #needs a case statement. better yet, smarter way to do this? (TODO)
    myavger=None
    if   pkg == 'cdo'            :
        from .cdoTimeAverager import cdoTimeAverager
        myavger=cdoTimeAverager(pkg = pkg, var=var,
                                unwgt = unwgt,
                                avg_type = avg_type, stddev_type = stddev_type)

    elif pkg == 'fre-nctools'    :
        from .frenctoolsTimeAverager import frenctoolsTimeAverager
        myavger=frenctoolsTimeAverager(pkg = pkg, var=var,
                                       unwgt = unwgt ,
                                       avg_type = avg_type, stddev_type = stddev_type)

    elif pkg == 'fre-python-tools':
        from .frepytoolsTimeAverager import frepytoolsTimeAverager
        myavger=frepytoolsTimeAverager(pkg = pkg, var=var,                           
                                       unwgt = unwgt,                                
                                       avg_type = avg_type, stddev_type = stddev_type)

    else :
        print('requested package unknown. exit.')
        return exitstatus

    if __debug__:
        print(f'myavger.__repr__={myavger.__repr__}')
    if myavger is not None:
        exitstatus=myavger.generate_timavg(infile=infile, outfile=outfile)
    else:
        print('ERROR: averager is None, check generate_time_average in generate_time_averages.py!')

    return exitstatus

def main():
    ''' main, for steering, when called like `python generate_time_averages.py` '''
    argparser = argparse.ArgumentParser(
        description='generate time averages for specified set of netCDF files. Example: \
        generate-time-averages.py /path/to/your/files/')
    argparser.add_argument('inf',
                           help='input file name',
                           type=str)
    argparser.add_argument('outf',
                           help='output file name',
                           type=str)
    argparser.add_argument('-p','--pkg',
                          help='time average approach',
                           type=str, choices=['cdo','fre-nctools','fre-python-tools'], default='cdo')
    argparser.add_argument('-v','--var',
                           help='specify variable to average',
                           type=str, default=None)
    argparser.add_argument('-u','--unwgt',
                           help='request unweighted statistics.',
                           action='store_true', default=False)
    argparser.add_argument('-a','--avg-type',
                           help='type of time average to generate. \n \
                                 currently, fre-nctools and fre-python-tools pkg options\n \
                                 do not support seasonal and monthly averaging.\n',
                           type=str, choices = ['month','seas','all'], default='all') 
    argparser.add_argument('-s','--stddev-type',
                           help='compute standard deviations for time-averages as well.',
                           type=str, choices=['samp','pop','samp_mean','pop_mean'], default='samp')
    # this kind of CLI functionality should be easy to add (TODO)
    #    argparser.add_argument('-st', '--stddev-type', 
    #                                 help='stddev type [pop, samp, meanpop, meansamp].\n \
    #                                       option is ignored unless --unwgt/-u is specified. \n \
    #                                       this functionality is still under construction.\n',
    #                           type=str, default=None)
    cli_args = argparser.parse_args()
    exitstatus=generate_time_average( cli_args.inf, cli_args.outf,
                                      cli_args.pkg, cli_args.var,
                                      cli_args.unwgt,
                                      cli_args.avg_type, cli_args.stddev_type)
    if exitstatus!=0:
        print(f'WARNING: exitstatus={exitstatus} != 0. Something exited poorly!')
    else:
        print('time averaging finished successfully')

if __name__ == '__main__':
    import time
    start_time=time.perf_counter()
    main()
    print(f'Finished in total time {round(time.perf_counter() - start_time , 2)} second(s)')
