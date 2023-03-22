need to imitate the time-averaging of Bronx files.

for files to compare to, take a peek at the files shown in Dana/Ciheim's excellent Bronx/Canopy comparison:
 - https://docs.google.com/spreadsheets/d/10FUuVGJo-f2RfTuJ_Jgr2BANOr571D2e-D53bUAtoGc/edit#gid=2001968637

files here I've already peeked at (not averaged files):
 - `/archive/Ciheim.Brown/am5/2022.01/c96L33_am5f1a0r0_amip/gfdl.ncrc4-intel21-prod-openmp/pp/atmos/ts/monthly/5yr/`

corresponding averaged files are here:
 - `/archive/Ciheim.Brown/am5/2022.01/c96L33_am5f1a0r0_amip/gfdl.ncrc4-intel21-prod-openmp/pp/atmos/av/monthly_5yr/`


cdo 
 - https://code.mpimet.mpg.de/projects/cdo/wiki

nco, of particular interest, `ncclimo`
 - https://nco.sourceforge.net/nco.html
 - https://nco.sourceforge.net/nco.html#ncclimo-netCDF-Climatology-Generator

fre-nctools, of particular interest, `timavg.csh` and `list_ncvars`
 - https://github.com/NOAA-GFDL/FRE-NCtools



_______________________ managing input file names for output names _______________________________
cute trick: basename into basename. first one removes the directory, second one remove the `.nc` ending... bash'ism?ztt
`basename -s .nc $(basename -a ls $TARGET_FILE_DIR)`










______________________ how does timavg.csh do it? ________________________________

well, in bronx, from a frepp script created when working on https://gitlab.gfdl.noaa.gov/fre2/workflows/postprocessing/-/issues/59
early in the "frepp_output_step1_noepmt" script, we see
   `set TIMAVG = "timavg.csh -mb"`

within `timavg.csh`, we see,
```
#!/bin/tcsh -f                                                                                                                                                                    
#                                                                                                                                                                                 
#***********************************************************************                                                                                                          
#                   GNU Lesser General Public License 

...
...

#  ----- parse input argument list ------                                                                                                                                                                                       

set argv = (`getopt abdmWo:v:w:r:z:s: $*`)

while ("$argv[1]" != "--")
    switch ($argv[1])
        case -a:
            set do_errors = .true.; breaksw
        case -b:
            set do_bounds = .true.; breaksw
        case -d:
            set debug; set do_verbose = .true.; breaksw
        case -m:
            set etime = .false.; breaksw

...
...

##################################################################                                                                                                                                    
#  ----- help message -----                                                                                                                                                                          

if ($ofile == "" || $#ifiles == 0) then
set name = `basename $0`
cat << EOF                                                                                                                                                                                                                       

Time averaging script                                                                                                                                                                                                            

Usage:  $name [-a] [-b] [-d] [-m] [-r prec] [-v vers] -o ofile  files.....                                                                                                                                                       
        -a       = skips "average information does not agree" errors                           
		-b       = adds time axis bounds and cell methods (CF convention)   
        -d       = turns on command echo (for debugging)                  
		-m       = average time (instead of end time) for t-axis values   
...
...

# executable name depends on precision     
if ($precision == 4) then
    set executable = `which TAVG.r4.exe`
else if ($precision == 8) then
    set executable = `which TAVG.exe`
else
    echo "ERROR: use -r4 or -r8"; exit 1
endif


...
...

#-- namelist (create unique name) --                                                                                                                                                                                           
set nml_name = nml`date '+%j%H%M%S%N'`
    echo " &input" > $nml_name
set i = 1
foreach file ($ifiles)
    echo "    file_names("$i") = " \'$file\' , >> $nml_name
    @ i++
end
    echo "    file_name_out = " \'$ofile\' ,     >> $nml_name
    echo "    use_end_time  = " $etime ,         >> $nml_name
    echo "    verbose  = " $do_verbose ,         >> $nml_name
    echo "    add_cell_methods = " $do_bounds ,  >> $nml_name
    echo "    skip_tavg_errors = " $do_errors ,  >> $nml_name
    echo "    suppress_warnings = " $no_warning, >> $nml_name

    if ($?weight) then
       echo "    frac_valid_data = " $weight ,   >> $nml_name
    endif

    if ($?deflation) then
       echo "    user_deflation = " $deflation ,   >> $nml_name
    endif

    if ($?shuffle) then
       echo "    user_shuffle = " $shuffle ,   >> $nml_name
    endif

    echo " &end"                                 >> $nml_name

#-- run averaging program --                                                                                                                                   

    $executable < $nml_name
    set exit_status = $status

#-- clean up --                     
rm -f $nml_name
exit $exit_status
```

