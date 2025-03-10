"""
Compute yearly (Water Year) aggregations for ParFlow and CLM outputs
"""
import numpy as np
from parflow.tools.io import read_pfb, write_pfb

monthly_dir = '<path/to/monthly/files>'
yearly_dir = '<path/to/save/yearly/files>'

water_year = 2024

# Define CONUS2 domain
nz = 10
ny = 3256
nx = 4442

dx = 1000
dy = 1000
dz = 200

# set p/q/r
p = 72
q = 48
r = 1

# Create crosswalk of start and end day indices for each month
# Assumption: day 001 is October 1 of the water year
# Assumption: remove 1 day from September due to time zone offsets causing the final day
# of the month to include hours from the following october and therefore not present if only
# a single WY of ParFlow outputs is available.
months = ['oct', 'nov', 'dec', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep']

if water_year % 4 == 0:
    days_in_month = [31, 30, 31, 31, 29, 31, 30, 31, 30, 31, 31, 29]
    days_in_year = 365
else:
    days_in_month = [31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31, 29]
    days_in_year = 364 

## indication for whether to calculate the mean (1) or the sum (0)
## The order here should correspond to the list made in `variables` 
variables = ['eflx_lh_tot', 'eflx_sh_tot', 'qflx_evap_grnd','qflx_tran_veg', 'qflx_evap_tot', 
             'swe_out', 't_grnd', 't_soil', 'press', 'satur', 
             'flow', 'SM', 'WTD', 'SURF_WATstorage', 'SUBstorage']
variables_mean = [1,1,0,0,0,
                  1,1,1,1,1,
                  1,1,1,1,1] 

# Loop through each variable and calculate yearly aggregation
for var_idx, var in enumerate(variables):
    if var == 't_soil':
        var_yearly = np.zeros((4,ny,nx))
    elif var in ['press', 'satur', 'SM', 'SUBstorage']:
        var_yearly = np.zeros((nz,ny,nx))
    else: 
        var_yearly = np.zeros((ny,nx))
    
    for m in range(0, 12):
        timestamp_reading = str(int(m+1)).rjust(2, '0')
        print(timestamp_reading)
        print(days_in_month[m])
        
        var_yearly += (read_pfb(f'{monthly_dir}/{var}.WY{water_year}.monthly.{timestamp_reading}.pfb').squeeze() * days_in_month[m])

    if variables_mean[var_idx] == 1:
        var_yearly /= days_in_year

    write_pfb(f'{yearly_dir}/{var}.WY{water_year}.yearly.pfb',var_yearly,dx=dx,dy=dy,dz=dz,P=p,Q=q,R=r,dist=False)
        