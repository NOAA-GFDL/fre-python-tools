from .timeAverager import timeAverager

class cdoTimeAverager(timeAverager): 
    '''
    class inheriting from abstract base class timeAverager
    generates time-averages using cdo (mostly, see weighted approach)
    '''
    
    def generate_timavg(self, infile=None, outfile=None):
        if __debug__:
            print(f'calling generate_cdo_timavg for file: {infile}')
            print(f'outfile={outfile}')
            print(f'stddev_type={self.stddev_type}')
            print(f'avg_type={self.avg_type}')
                
        if all([self.avg_type!='all',self.avg_type!='seas',self.avg_type!='month',
                self.avg_type is not None]):
            print(f'ERROR, avg_type requested unknown.')
            return 1

        from cdo import Cdo
        _cdo=Cdo()
        
        N_time_bnds=-1
        wgts_sum=0
        if not self.unwgt: #weighted case, cdo ops alone don't support a weighted time-average.
            from netCDF4 import Dataset
            import numpy
            
            nc_fin = Dataset(infile, 'r')
            time_bnds=nc_fin['time_bnds'][:].copy()
            N_time_bnds=len(time_bnds)
            
            wgts=numpy.moveaxis(time_bnds,0,-1)[1][:].copy() - numpy.moveaxis(time_bnds,0,-1)[0][:].copy()
            wgts_sum=sum(wgts)
            
            if __debug__:
                print(f'wgts_sum={wgts_sum}')
                
                nc_fin.close()
                
        if self.avg_type == 'all':
            if not self.stddev: 
                print(f'time average over all time requested.')
                if self.unwgt:
                    _cdo.timmean(input=infile, output=outfile, returnCdf=True)
                else:
                    _cdo.divc( str(wgts_sum), input="-timsum -muldpm "+infile, output=outfile)
                
                print(f'done averaging over all time.')
            else:
                print(f'time standard-deviation (N-1) over all time requested.')
                _cdo.timstd1(input=infile, output=outfile, returnCdf=True)
                print(f'done computing standard-deviation over all time.')
            
        elif self.avg_type == 'seas':
            if not self.stddev:
                print(f'seasonal time-averages requested.')
                _cdo.yseasmean(input=infile, output=outfile, returnCdf=True)
                print(f'done averaging over seasons.')
            else:
                print(f'seasonal time standard-deviation (N-1) requested.')
                _cdo.yseasstd1(input=infile, output=outfile, returnCdf=True)
                print(f'done averaging over seasons.')
            
        elif self.avg_type == 'month':
            if not self.stddev:
                print(f'monthly time-averages requested.')
                _cdo.ymonmean(input=infile, output=outfile, returnCdf=True)
                print(f'done averaging over months.')
            else:
                print(f'monthly time standard-deviation (N-1) requested.')
                _cdo.ymonstd1(input=infile, output=outfile, returnCdf=True)
                print(f'done averaging over months.')
            
        else:
            print(f'problem: unknown avg_type={self.avg_type}')
            return 1
        
        print(f'done averaging')
        return 0
