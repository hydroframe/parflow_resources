"""
Process and save ParFlow hourly overland flow
"""
import os
import numpy as np
from parflow.tools.io import read_pfb, write_pfb
import parflow.tools.hydrology as hydro

### DEFINE WATER YEAR, START DAY, & END DAY ###
water_year = 2024

### DEFINE PATHS ###
path_outputs = '<path/to/raw/parflow/outputs>'
runname = '<pf_run_name>'
directory_out = '<path/for/saving/hourly/flow>'
print(f'Saving hourly flow to: {directory_out}')

### READING ALL STATIC VARIABLES AND DOMAIN INFO NEEDED ###
mannings = read_pfb(f'{path_outputs}/{runname}.out.mannings.pfb')
slopex = read_pfb(f'{path_outputs}/{runname}.out.slope_x.pfb')
slopey = read_pfb(f'{path_outputs}/{runname}.out.slope_y.pfb')

## formatting the mask so that values outside the domain are NA and inside the domain are 1
mask = read_pfb(f'{path_outputs}/{runname}.out.mask.pfb')
active_mask=mask.copy()
active_mask[active_mask > 0] = 1

nz = 10
ny = 3256
nx = 4442

dx = 1000
dy = 1000
dz = 200
dz_3d = np.array([2.0e+02, 1.0e+02, 5.0e+01, 2.5e+01, 1.0e+01, 5.0e+00, 1.0e+00, 6.0e-01, 3.0e-01, 1.0e-01])

# this is currently the same processor topology CONUS2 was run on Cheyenne
p = 72
q = 48
r = 1

### COMPUTE FLOW AND SAVE PFB FILES ### 
  
# read pressure at timestep
hour_idx = int(os.environ["SLURM_ARRAY_TASK_ID"]) + 8000
timestamp_reading = str(int(hour_idx)).rjust(5, '0')
pressure = read_pfb(f'{path_outputs}{runname}.out.press.{timestamp_reading}.pfb') * active_mask
print(f'reading {path_outputs}{runname}.out... at time {timestamp_reading}')
       
## Calculate Flow 
overland_flow = hydro.calculate_overland_flow_grid(pressure, slopex, slopey, mannings, dx, dy, mask = active_mask)
                           
## Save to pfb
write_pfb(f'{directory_out}/{runname}.out.flow.{timestamp_reading}.pfb', overland_flow, dx=dx,dy=dy,dz=dz,P=p,Q=q,R=r,dist=False)
