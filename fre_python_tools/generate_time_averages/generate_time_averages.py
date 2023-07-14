#!/usr/bin/env python
''' tools for generating time averages from various packages '''
import argparse

def generate_time_average(pkg=None, infile=None, outfile=None, avg_type=None,
                          unwgt=False, stddev=False, stddev_type=None):
    ''' steering function to various averaging functions above'''
    if __debug__:
        print(f'calling generate time averages for file: {infile}')
    exitstatus=1

    #needs a case statement
    myavger=None
    if   pkg == 'cdo'            :
        from .cdoTimeAverager import cdoTimeAverager
        myavger=cdoTimeAverager(pkg=pkg, avg_type=avg_type,
                                unwgt=unwgt,stddev=stddev,stddev_type=stddev_type)

    elif pkg == 'fre-nctools'    :
        from .frenctoolsTimeAverager import frenctoolsTimeAverager
        myavger=frenctoolsTimeAverager(pkg=pkg, avg_type=avg_type,
                                       unwgt=unwgt,stddev=stddev,stddev_type=stddev_type)

    elif pkg == 'fre-python-tools':
        from .frepytoolsTimeAverager import frepytoolsTimeAverager
        myavger=frepytoolsTimeAverager(pkg=pkg, avg_type=avg_type,
                                      unwgt=unwgt,stddev=stddev,stddev_type=stddev_type)

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
                          help='time average approach [cdo, fre-nctools, fre-python-tools]',
                          type=str, default='cdo')
    argparser.add_argument('-a','--avg-type',
                           help='type of time average to generate [e.g. month,seas,all].\n \
                                 currently, fre-nctools and fre-python-tools pkg options\n \
                                 do not support seasonal and monthly averaging.\n',
                          type=str, default='all')
    argparser.add_argument('-u','--unwgt',
                           help='compute requested statistics with no weights.',
                           action='store_true', default=False)
    argparser.add_argument('-s','--stddev',
                           help='compute standard deviations for time-averages as well.',
                           action='store_true', default=False)
    argparser.add_argument('-st', '--stddev-type',
                                 help='specify type of stddev to compute [pop, samp, meanpop, meansamp].\n \
                                       this option is meaningless/ignored unless unweighted statistics \n \
                                       are requested. this functionality is still under construction.\n',
                           type=str, default=None)
    cli_args = argparser.parse_args()
    exitstatus=generate_time_average( cli_args.pkg, cli_args.inf, cli_args.outf, cli_args.avg_type ,
                                      cli_args.unwgt, cli_args.stddev, cli_args.stddev_type)
    if exitstatus!=0:
        print(f'WARNING: exitstatus={exitstatus} != 0. Something exited poorly!')
    else:
        print('time averaging finished successfully')

if __name__ == '__main__':
    import time
    start_time=time.perf_counter()
    main()
    finish_time=time.perf_counter()
    print(f'Finished in total time {round(finish_time - start_time , 2)} second(s)')
