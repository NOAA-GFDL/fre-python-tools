from .timeAverager import timeAverager

class frenctoolsTimeAverager(timeAverager):
    '''
    class inheriting from abstract base class timeAverager
    generates time-averages using fre-nctools
    '''
    #assert(self.pkg=='fre-nctools)' #don't do this, use property decorator.
                                     #see 7.17 in python distilled.
                                     #maybe put in base class?
    #@property
    #def pkg(self):
    #return self._pkg

#    def just_say_hello():             #error: takes 0 positional arguments but 1 was given
#        print('HELLOOOOO CLASSES!!!!')# b.c. self is passed as an arg automatically.
#
#    def just_say_hello(self): #self is req'd as an arg here. b.c. it always get's passed, unless...
#        print('HELLOOOOO CLASSES!!!!')
#
#    @staticmethod # you use a static method signified, so self isn't passed as an arg automatically.
#    def just_say_hello2():
#        print('(static) HELLOOOOO CLASSES!!!!')

    def generate_timavg(self, infile=None, outfile=None):
        ''' use fre-nctool's CLI timavg.csh with subprocess call '''
        if __debug__:
            print(f'calling generate_frenctools_timavg for file: {infile}')



        # class settings, check consistency with current class capabilities
        exitstatus=1
        if self.avg_type!='all':
            print(f'ERROR: avg_type={avg_type} is not supported by this function at this time.')
            return exitstatus

        if self.unwgt:
            print(f'WARNING: unwgt=True unsupported by frenctoolsAverager. ignoring!!!')

        if self.stddev:
            print(f'WARNING: stddev=True unsupported by frenctoolsTimeAverager. ignoring!!!')

        if self.stddev_type is not None:
            print(f'WARNING: stddev_type arg unsupported by frenctoolsTimeAverager. ignoring!!!')

        # input arg checks
        if infile is None:
            print(f'ERROR: I need an input file, specify a value for the infile argument')
            return exitstatus

        if outfile is None:
            outfile='frenctoolsTimeAverage_'+infile
            print(f'WARNING: no output filename given, setting outfile={outfile}')

        from subprocess import Popen, PIPE

        precision='-r8'
        timavgcsh_command=['timavg.csh', precision, '-mb','-o', outfile, infile]
        exitstatus=1
        with Popen(timavgcsh_command,
                   stdout=PIPE, stderr=PIPE, shell=False) as subp:
            output=subp.communicate()[0]
            print(f'output={output}')

            if subp.returncode < 0:
                print('error')
            else:
                print('success')
                exitstatus=0

        return exitstatus
''' class for utilizing timavg.csh (aka script to TAVG fortran exe) in frenc-tools '''
