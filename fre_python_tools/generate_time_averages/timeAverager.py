''' core class structure for this module.'''

class timeAverager:
    '''
    abstract base class for generating time averages + related statistical quantities
    this class must be inherited by another for functionality.
    '''
    pkg: str
    avg_type: str
    unwgt: bool
    stddev: bool
    stddev_type: str

    def __init__(self): #init method 1, no inputs given
        self.pkg = "cdo"
        self.avg_type = "all" #may also be, "fre-python-tools" or "fre-nctools"
        self.unwgt = False
        self.stddev = False
        self.stddev_type = "sample" #may also be, "population". only relevant if unwgt = False

    def __init__(self, pkg, avg_type, unwgt,
                 stddev, stddev_type): #init method 2, all inputs specified
        self.pkg = pkg
        self.avg_type = avg_type
        self.unwgt = unwgt
        self.stddev = stddev
        self.stddev_type = stddev_type

    def __repr__(self):
        return f'{type(self).__name__}( pkg={self.pkg}, \
                               avg_type={self.avg_type}, \
                               unwgt={self.unwgt}, \
                               stddev={self.stddev}, \
                               stddev_type={self.stddev_type})'

    # this is here as a hint: this function is to be defined by classes inheriting from this abstract one.
    # this function is never to be fully defined here by design.
    def generate_timavg(self, infile=None, outfile=None):
        raise NotImplementedError()
