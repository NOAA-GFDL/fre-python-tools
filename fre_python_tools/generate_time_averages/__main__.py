#!/usr/bin/env python
import argparse
import os, sys


def main():
    print('hello world, from generate-time-averages!')


    parser = argparse.ArgumentParser(description="generate time averages for specified set of netCDF files. Example: \
    generate-time-averages.py /path/to/your/files/")
    parser.add_argument('-h', '--help',
                        help="display help summary of options and usage examples.")
    
    args = parser.parse_args()    
    
    return
    
if __name__ == "__main__":
    sys.exit(main())
