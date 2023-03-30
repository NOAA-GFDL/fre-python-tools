#!/bin/sh

# little script to help keep me oriented.
# for dev purposes only, will be removed in final implementation

module load git
module load python
#module load ncview
module load fre-nctools

# ________________________________
## default cdo package, v 1.9.10 [can use this or other 1.X.Y versions through python]
module load cdo

# non-default, cdo v 2.1.0 [no python package for this version yet though]
#module load cdo/2.1.0

### install cdo package in user conda env
#pip install cdo --user

# ________________________________
## default nco package, v 5.0.1
#module load nco

#ncclimo

# ________________________________
## default, 2022.02
#module load fre-nctools

## see CLI usage in timavgcsh_CLI.sh
#timavg.csh


