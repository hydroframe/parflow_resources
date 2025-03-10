"""
Compute monthly aggregations for ParFlow and CLM outputs
"""
import os
import numpy as np
from parflow.tools.io import read_pfb, write_pfb

daily_dir = '<path/to/daily/parflow/files>'
monthly_dir = '<path/to/save/monthly/files>'

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

month_idx = int(os.environ["SLURM_ARRAY_TASK_ID"])
month = months[month_idx]

if water_year % 4 == 0:
    days_in_month = [31, 30, 31, 31, 29, 31, 30, 31, 30, 31, 31, 29]
else:
    days_in_month = [31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31, 29]

month_start = sum(days_in_month[:month_idx])+1
month_end = sum(days_in_month[:month_idx+1])
print(f'Month: {month}, days: {month_start} to {month_end}')

## indication for whether to calculate the mean (1) or the sum (0)
## The order here should correspond to the list made in `variables` 
variables = ['eflx_lh_tot', 'eflx_sh_tot', 'qflx_evap_grnd','qflx_tran_veg', 'qflx_evap_tot', 
             'swe_out', 't_grnd', 't_soil', 'press', 'satur', 
             'flow', 'SM', 'WTD', 'SURF_WATstorage', 'SUBstorage']
variables_mean = [1,1,0,0,0,
                  1,1,1,1,1,
                  1,1,1,1,1] 

# Loop through each CLM variable and calculate monthly aggregation
for var_idx, var in enumerate(variables):
    if var == 't_soil':
        var_monthly = np.zeros((4,ny,nx))
    elif var in ['press', 'satur', 'SM', 'SUBstorage']:
        var_monthly = np.zeros((nz,ny,nx))
    else: 
        var_monthly = np.zeros((ny,nx))
    
    for d in range(month_start, month_end+1):
        timestamp_reading = str(int(d)).rjust(3, '0')
        print(timestamp_reading)
        
        var_monthly += read_pfb(f'{daily_dir}/{var}.{water_year}.daily.{timestamp_reading}.pfb').squeeze()

    if variables_mean[var_idx] == 1:
        var_monthly /= days_in_month[month_idx]

    month_fmt = str(int(month_idx+1)).rjust(2, '0')
    write_pfb(f'{monthly_dir}/{var}.WY{water_year}.monthly.{month_fmt}.pfb',var_monthly,dx=dx,dy=dy,dz=dz,P=p,Q=q,R=r,dist=False)
        