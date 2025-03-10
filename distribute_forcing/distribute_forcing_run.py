"""
distribute forcing files
"""
from parflow.tools import Run

#-----------------------------------------------------------------------------------------
# User-defined local variables
#-----------------------------------------------------------------------------------------

runname = '<parflow_runname>'
forcing_path = 'path/to/forcing/files'
base = 'path/to/forcing/files'
var_list = ['APCP', 'DLWR', 'DSWR', 'Temp', 'SPFH', 'UGRD', 'VGRD', 'Press']


# Define ParFlow Run information
dt = 24
CONUS2 = Run(runname, __file__)
CONUS2.FileVersion = 4
CONUS2.Process.Topology.P = 70
CONUS2.Process.Topology.Q = 48
CONUS2.Process.Topology.R = 1

for var in var_list:
    for i in range(0, 8760, dt):
        data = 'CW3E.'+var+"."+f"{i:06d}"+'_to_'+f"{(i+dt-1):06d}"+'.pfb'
        CONUS2.dist(base+data)
