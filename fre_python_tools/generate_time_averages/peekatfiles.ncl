


f_in = addfile("/archive/Ciheim.Brown/am5/2022.01/c96L33_am5f1a0r0_amip/gfdl.ncrc4-intel21-prod-openmp/pp/atmos/ts/monthly/5yr/atmos.197901-198312.omega.nc","r")

atts_f_in=getvaratts(f_in)
print(atts_f_in)




f_out = addfile("./test.nc","r")
atts_f_out=getvaratts(f_out)
print(atts_f_out)