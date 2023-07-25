''' core class structure for this module.'''

class timeAverager:
    '''
    abstract base class for generating time averages + related statistical quantities
    this class must be inherited by another for functionality.
    '''
    pkg: str
    var: str
    unwgt: bool
    avg_type: str
    stddev_type: str

    def __init__(self): #init method 1, no inputs given
        self.pkg = "cdo"
        self.var = None
        self.unwgt = False
        self.avg_type = "all" #see argparser for options
        self.stddev_type = None #see argparser for options
                               
    def __init__(self, pkg, var, unwgt,
                 avg_type, stddev_type): #init method 2, all inputs specified
        self.pkg = pkg
        self.var = var
        self.unwgt = unwgt
        self.avg_type = avg_type
        self.stddev_type = stddev_type

    def __repr__(self):
        return f'{type(self).__name__}( pkg={self.pkg}, \
                               unwgt={self.unwgt}, \
                               var={self.var}, \
                               avg_type={self.avg_type}, \
                               stddev_type={self.stddev_type})'

    def generate_timavg(self, infile=None, outfile=None):
        '''# this is a hint: this is to be defined by classes inheriting from the abstract one
        this function is never to be fully defined here by design.'''
        raise NotImplementedError()
