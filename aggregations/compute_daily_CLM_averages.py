"""
###########################################
### Process and save CLM daily averages
###########################################

# This script takes hourly CLM outputs as PFB files and computes the daily aggregations
# to be saved as PFB files.
# DTT & EL, 10/2022
# Updated 01/2025 by AD for use in new CONUS2.1 model

# Inputs:
# - Directory where CLM outputs are and directory where you want to save output
# - Hourly PFB files of CLM outputs
# - Water year and day start/end

# Outputs:
# - PFB files for daily average of each USER SELECTED variable. This is defined with `variables_clm`  
# - The outputs important for CONUS2 (DTT, from MMF CONUS1 outputs)  
#     - Latent heat (LH) – CLM out layer 1 [W/m^2]
#     - Sensible heat flux (SH) – CLM out layer 3 [W/m^2]
#     - ground evaporation without condensation (qflx_grnd) – CLM out layer 6 [mm/s]
#     - Vegetation transpiration (qflx_trans) – CLM out layer 9 [mm/s]
#     - Snow water equivalent (SWE) – CLM out layer 11 [mm]
#     - Ground temperature (Tgrnd) – CLM out layer 12 [K] skin temp
#     - Soil temperature (Tsoil) – CLM out layer 14 - last layer [K] *** This script outputs all soil temp layers as a 3D array
#     - Total evapotranspiration (qflx_evap_tot) - CLM out layer 5 [mm/s] *** NOT converted in this script  


# Notes (10/23/22):  
# - ET from qflx_evap_tot is just the direct CLM output. Do we want to convert this here? Is there a different way we want to calculate ET? 
#   (PFTools' `calculate_evapotranspiration` currently has weird units, so was recommended against using this).  
#   - Kept the ET calculation in as a comment, but you don't need this here because you can just output `qflx_evap_tot`
# - Soil Temp in this script is saved as a 3D array (temp for each soil layer), which is different than the Fortran scripts 
#   which only saved the CLM layer 14, temp @5cm

# Note: Line 112 implements an hourly offset of 6 hours in order to more closely align with local time across the CONUS2 domain
"""
import os
import numpy as np
from parflow.tools.io import read_pfb,write_pfb

# CONUS2.0 run is 13 + 4
# NCLMOUTPUTS = 13 + 4     # 13 (number variables) + number of layers over which CLM is active, NZ root

# CONUS2.1 run is 13 + 5
NCLMOUTPUTS = 13 + 5      # 13 (number variables) + number of layers over which CLM is active, NZ root

### DEFINE WATER YEAR
water_year = 2003

### DEFINE PATHS ###
## path to CLM hourly outputs
path_outputs = '<path/to/raw/parflow/outputs>'

## PFCLM run name
runname = '<pf_run_name>'

## directory to save averages to
directory_out = '<path/for/saving/aggregations>'
print(f'Saving averages to: {directory_out}')

### READING ALL STATIC VARIABLES AND DOMAIN INFO NEEDED ###
#### CONUS2 #######
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

### DEFINE CLM AVERAGES TO BE COMPUTED ###
#list of clm variables you want
variables_clm = ['eflx_lh_tot', 'eflx_sh_tot', 'qflx_evap_grnd','qflx_tran_veg', 'qflx_evap_tot', 'swe_out', 't_grnd', 't_soil']

## indication for whether you want the mean (1) or the sum (0)
## The order here should correspond to the list made in `variables_clm`
variables_clm_mean = [1,1,0,0,0,1,1,1] 

# List of all variables in CLM file
ALL_CLM = ['eflx_lh_tot','eflx_lwrad_out','eflx_sh_tot','eflx_soil_grnd','qflx_evap_tot','qflx_evap_grnd','qflx_evap_soi','qflx_evap_veg','qflx_tran_veg','qflx_infl','swe_out','t_grnd','qflx_qirr','t_soil']

### CLM Outputs for reference ###
# eflx_lh_tot    # CLM 1 / Py[0]   # latent heat flux total [W/m2] using the silo variable LatentHeat;
# eflx_lwrad_out # CLM 2 / Py[1]   # outgoing long-wave radiation [W/m2] using the silo variable LongWave;
# eflx_sh_tot    # CLM 3 / Py[2]   # sensible heat flux total [W/m2] using the silo variable SensibleHeat;
# eflx_soil_grnd # CLM 4 / Py[3]   # ground heat flux [W/m2] using the silo variable GroundHeat;
# qflx_evap_tot  # CLM 5 / Py[4]   # total evaporation [mm/s] using the silo variable EvaporationTotal;
# qflx_evap_grnd # CLM 6 / Py[5]   # ground evaporation without condensation [mm/s] using the silo variable EvaporationGround- NoSublimation;
# qflx_evap_soi  # CLM 7 / Py[6]   # soil evaporation [mm/s] using the silo variable EvaporationGround;
# qflx_evap_veg  # CLM 8 / Py[7]   # vegetation evaporation (canopy) and transpiration (mms-1) using the silo variable EvaporationCanopy;
# qflx_tran_veg  # CLM 9 / Py[8]   # vegetation transpiration [mm/s] using the silo variable Transpiration;
# qflx_infl      # CLM 10 / Py[9]  # soil infiltration [mm/s] using the silo variable Infiltration;
# swe_out        # CLM 11 / Py[10] # snow water equivalent [mm] using the silo variable SWE;
# t_grnd         # CLM 12 / Py[11] # ground surface temperature [K] using the silo variable TemperatureGround;
# qflx_qirr      # CLM 13 / Py[12] # irrigation flux
# t_soil         # CLM 14-top layer #soil temperature by layer


### COMPUTE AVERAGES AND SAVE PFB FILES ###
day_idx = int(os.environ["SLURM_ARRAY_TASK_ID"])
timestamp_day_out = str(int(day_idx+1)).rjust(3, '0')

## INITIALIZE WHATEVER DYNAMIC VARIABLES THAT NEED HOURLY READING     
if not variables_clm == False:
    clm_output = np.zeros((NCLMOUTPUTS,ny,nx))
for h in range(day_idx*24+1+6,(day_idx+1)*24+1+6): #For UTC: day*24+1,(day+1)*24+1
    timestamp_reading = str(int(h)).rjust(5, '0')

    # CLM Variables
    clm_output += read_pfb(f'{path_outputs}{runname}.out.clm_output.{timestamp_reading}.C.pfb')
    print(f'reading {path_outputs}{runname}.out.clm_output.{timestamp_reading}.C.pfb')

# Compute averages CLM outputs
for ind_clm in range(len(variables_clm)):

    # Check if it's t_soil, then it's 3D!
    if variables_clm[ind_clm] == 't_soil':
        clm_save = clm_output[14:,:,:]
    else:
        ind_in_clmoutput = ALL_CLM.index(variables_clm[ind_clm])
        clm_save = clm_output[ind_in_clmoutput,:,:]
    if variables_clm_mean[ind_clm]==1:
        clm_save/=24

    # SAVE VARIABLES CLM outputs
    write_pfb(f'{directory_out}/{variables_clm[ind_clm]}.{water_year}.daily.{timestamp_day_out}.pfb',clm_save,dx=dx,dy=dy,dz=dz,P=p,Q=q,R=r,dist=False)
