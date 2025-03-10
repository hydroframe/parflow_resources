"""
###########################################
### Process and save ParFlow daily averages
###########################################

# This script takes hourly PF outputs as PFB files and computes the daily averages to be saved as PFB files.
# DTT & EL, 10/2022
# Updated 01/2025 by AD for use in new CONUS2.1 model

# Inputs:
# - Directory where PF outputs are and directory where you want to save output
# - Hourly PFB files of PF outputs
# - Water year and day start/end

# Outputs:
# - PFB files for daily average of each variable:  
#     - Overland flow at each grid cell (flow) [m^3/h]   
#     - Soil moisture (SM) [-]  
#     - Water table depth (WTD) [m]   
#     - Surface water storage (SURF_WATstorage) [m^3]
#     - Total Subsurface Storage (SUBstorage) [m^3]  
#       - *** To note, the output of SUBstorage is a 3D array of storage for each subsurface layer, 
#       so the GW storage and SM storage can be computed from those files at a later time. Additionally, in order to 
#       compute the TOTAL subsurface storage, one must sum all layers for these arrays. This is different 
#       from the postprocessing done using the Fortran files, where each of the storage components had to be 
#       computed and saved up front. 
   
    
# Notes (10/21/22):
# - Need to add in monthly and yearly averages - Created new script for this since we are processing one month at a time `Compute_month-year_averages_PFCLM.ipynb`
# - *Need to figure out the GW and SM Storage (which layers, do we even want to separate by layer, do by WTD???)
#   - Idea: Create mask from WTD (above and below)?
#   - Don't need to super worry about this now, since the Total Subsurface Storage is a 3D array with storage in each layer. We can calculate GWstorage and SMstorage later. 

# Note: Line 99 implements an hourly offset of 6 hours in order to more closely align with local time across the CONUS2 domain
"""
import os
import numpy as np
from parflow.tools.io import read_pfb,write_pfb
import parflow.tools.hydrology as hydro

### DEFINE WATER YEAR###
water_year = 2003

### DEFINE PATHS ###
## path to PF hourly outputs
path_outputs = '<path/to/raw/parflow/outputs>'

## PFCLM run name
runname = '<pf_run_name>'

## directory to save averages to
directory_out = '<path/for/saving/aggregations>'
print(f'Saving averages to: {directory_out}')


### READING ALL STATIC VARIABLES AND DOMAIN INFO NEEDED ###
porosity = read_pfb(f'{path_outputs}/{runname}.out.porosity.pfb')
specific_storage = read_pfb(f'{path_outputs}/{runname}.out.specific_storage.pfb')
mannings = read_pfb(f'{path_outputs}/{runname}.out.mannings.pfb')
slopex = read_pfb(f'{path_outputs}/{runname}.out.slope_x.pfb')
slopey = read_pfb(f'{path_outputs}/{runname}.out.slope_y.pfb')

## formatting the mask so that values outside the domain are NA and inside the domain are 1
mask = read_pfb(f'{path_outputs}/{runname}.out.mask.pfb')
active_mask=mask.copy()
active_mask[active_mask > 0] = 1

## DEFINE CONUS2 DOMAIN
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


### COMPUTE AVERAGES AND SAVE PFB FILES ###
day_idx = int(os.environ["SLURM_ARRAY_TASK_ID"])
timestamp_day_out = str(int(day_idx+1)).rjust(3, '0')

##INITIALIZE WHATEVER DYNAMIC VARIABLES THAT NEED HOURLY READING
pressure_daily = np.zeros((nz,ny,nx))           # Pressure
saturation_daily = np.zeros((nz,ny,nx))         # Saturation
overland_flow = np.zeros((ny, nx))              # Flow
soil_moisture = np.zeros((nz,ny,nx))            # Soil Moisture
wtd = np.zeros((ny, nx))                        # Water Table Depth
surface_storage = np.zeros((ny,nx))             # Surface Water Storage
subsurface_storage = np.zeros((nz,ny,nx))       # Total Subsurface Storage


for h in range(day_idx*24+1+6,(day_idx+1)*24+1+6): # FOR UTC TIME: range(day*24+1,(day+1)*24+1):

    timestamp_reading = str(int(h)).rjust(5, '0')
        
    # read pressure and saturation at timestep 
    saturation = read_pfb(f'{path_outputs}{runname}.out.satur.{timestamp_reading}.pfb') * active_mask
    pressure = read_pfb(f'{path_outputs}{runname}.out.press.{timestamp_reading}.pfb') * active_mask
    print(f'reading {path_outputs}{runname}.out... at time {timestamp_reading}')
        
    ##################
    ## Computations ##
    ##################
    
    ## Pressure and saturation
    pressure_daily += pressure
    saturation_daily += saturation
    
    ## Flow 
    overland_flow += hydro.calculate_overland_flow_grid(pressure, slopex, slopey, mannings, dx, dy, mask = active_mask)
        
    ## Soil Moisture [-]
    soil_moisture += saturation * porosity
        
    ## Water Table Depth
    wtd += hydro.calculate_water_table_depth(pressure, saturation, dz_3d)
        
    ## Surface Storage
    ## total surface storage for this time step is the summation of substorage surface across all x/y slices
    surface_storage += hydro.calculate_surface_storage(pressure, dx, dy, mask = active_mask)
        
    # Total Subsurface Storage
    subsurface_storage += hydro.calculate_subsurface_storage(porosity, pressure, saturation, specific_storage, dx, dy, dz_3d, mask = active_mask)

               
### compute daily average ###
pressure_daily /= 24
saturation_daily /= 24
overland_flow /= 24
soil_moisture /= 24
wtd /= 24 
surface_storage /= 24
subsurface_storage /= 24
    
### SAVE VARIABLES AS PFB FILES
write_pfb(f'{directory_out}/press.{water_year}.daily.{timestamp_day_out}.pfb',pressure_daily,dx=dx,dy=dy,dz=dz,P=p,Q=q,R=r,dist=False)
write_pfb(f'{directory_out}/satur.{water_year}.daily.{timestamp_day_out}.pfb',saturation_daily,dx=dx,dy=dy,dz=dz,P=p,Q=q,R=r,dist=False)

write_pfb(f'{directory_out}/flow.{water_year}.daily.{timestamp_day_out}.pfb',overland_flow,dx=dx,dy=dy,dz=dz,P=p,Q=q,R=r,dist=False)
write_pfb(f'{directory_out}/SM.{water_year}.daily.{timestamp_day_out}.pfb',soil_moisture,dx=dx,dy=dy,dz=dz,P=p,Q=q,R=r,dist=False)
write_pfb(f'{directory_out}/WTD.{water_year}.daily.{timestamp_day_out}.pfb',wtd,dx=dx,dy=dy,dz=dz,P=p,Q=q,R=r,dist=False)
write_pfb(f'{directory_out}/SURF_WATstorage.{water_year}.daily.{timestamp_day_out}.pfb',surface_storage,dx=dx,dy=dy,dz=dz,P=p,Q=q,R=r,dist=False)
write_pfb(f'{directory_out}/SUBstorage.{water_year}.daily.{timestamp_day_out}.pfb',subsurface_storage,dx=dx,dy=dy,dz=dz,P=p,Q=q,R=r,dist=False)
