cmor
Climate Model Output Rewriter is used to produce CF-compliant netCDF files. The structure of the files created by the library and the metadata they contain fulfill the requirements of many of the climate community's standard model experiments.
CMOR can be considered a general purpose rewriter, agnostic to particular standards such as CMIP6. It accepts an configuration file that describes the output file name, global attributes, variable attributes, dimension names, and more. Example template files are included that adhere roughly to CMIP6 specifications. They may be modified to conform to other specifications.
In current suite there are 2 variants of input data represented - monthly and daily for whole sphere. There are also another timeperiods data: 1hr,3hr,6hr,yr. They all can be for different type of surface - land, ocean.

Getting Started
These CMOR scripts may be used to rewrite a set of NetCDF files (standard GFDL post-process output) to be publishing-ready,
especially for CMIP6. As an example, the post-process output of the DECK/1pctCO2 experiment run by the GFDL-CM4 model is here:

/archive/oar.gfdl.cmip6/CM4/warsaw_201710_om4_v1.0.1/CM4_1pctCO2_C/gfdl.ncrc4-intel16-prod-openmp/pp
and the published CMIP6 output (processed using fremetar/Curator tool) is here:

/archive/uda/CMIP6/CMIP/NOAA-GFDL/GFDL-CM4/1pctCO2

Check-out this CMOR app tool


Clone this repository
Using SSH 

git clone git@github.com:NOAA-GFDL/fre-python-tools.git

or using HTTPS

https://github.com/NOAA-GFDL/fre-python-tools.git

cd cmor

Load the PCMDI CMOR package


module load conda
conda activate cmor

See command-line usage help


python cmor_commander.py --help

usage: cmor_commander.py [-h] -d DIR2CMOR -l GFDL_VARS_FILE -r CMOR_TBL_JSON -p CMIP_INPUT_JSON [-o CMIP_OUTPUT]

CMORizing all files in directory specified in command line

options:
  -h, --help          show this help message and exit
  -d DIR2CMOR         directory to CMORize
  -l GFDL_VARS_FILE   GFDL list of variables in table
  -r CMOR_TBL_JSON    CMOR file with CMIP descriptions of variables
  -p CMIP_INPUT_JSON  Experiment Name File expaining of what source type is used here
  -o CMIP_OUTPUT      CMORized output files location (not required), default=/local2; it also can be like /home/$USER, or
                      /net|work<i>/san, etc.
The next steps will identify the input configuration files needed for the -l, -r, and -p flags.

Download template "User Input File" (for the -p option)

This is a JSON file that contains experiment-specific metadata and configuration directives.

wget https://raw.githubusercontent.com/PCMDI/cmip6-cmor-tables/master/Tables/CMIP6_input_example.json
You may edit the file or leave it as-is for an initial test.

Download CMIP6 CV for the desired variable group (e.g. Amon, Omon, day, etc); for the -r option.


wget https://raw.githubusercontent.com/PCMDI/cmip6-cmor-tables/master/Tables/CMIP6_Amon.json
The "Amon" variable group chosen here is the monthly atmosphere set.

Download three additional CMIP6 CV files (to the same location as the CMIP6 table)


wget https://raw.githubusercontent.com/PCMDI/cmip6-cmor-tables/master/Tables/CMIP6_coordinate.json
wget https://raw.githubusercontent.com/PCMDI/cmip6-cmor-tables/master/Tables/CMIP6_formula_terms.json
wget https://raw.githubusercontent.com/PCMDI/cmip6-cmor-tables/master/Tables/CMIP6_CV.json

Create input variable list, and optionally rename variables (for the -l option)

Create a JSON file (variables.json) with this structure:

{
    "var1in" : "var1out",
    "var2in" : "var2out",
    "var3in" : "var3out"
}
For this test case, we will choose this atmosphere/monthly location and two variables.

/archive/oar.gfdl.cmip6/CM4/warsaw_201710_om4_v1.0.1/CM4_1pctCO2_C/gfdl.ncrc4-intel16-prod-openmp/pp/atmos_cmip/ts/monthly/5yr

{
    "psl" : "psl",
    "tas" : "tas"
}

If your input files are on tape archive, then request them using dmget first:


dmget /archive/oar.gfdl.cmip6/CM4/warsaw_201710_om4_v1.0.1/CM4_1pctCO2_C/gfdl.ncrc4-intel16-prod-openmp/pp/atmos_cmip/ts/monthly/5yr/*.{tas,psl}.nc &
The tape migration will be done in the background with the &.

Run the CMOR tool!

The output location (-o) can be any directory that you can write to.

    python cmor_commander.py \
        -d /archive/oar.gfdl.cmip6/CM4/warsaw_201710_om4_v1.0.1/CM4_1pctCO2_C/gfdl.ncrc4-intel16-prod-openmp/pp/atmos_cmip/ts/monthly/5yr \
        -l variables.json \
        -r CMIP6_Amon.json \
        -p CMIP6_input_example.json \
        -o /local2/home/cmor-test-output
If the postprocess files are available, the processing should not take too long. There are about ~720 MB to process in this example.

Examine output files
