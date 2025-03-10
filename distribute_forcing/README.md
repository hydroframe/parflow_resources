# distribute_forcing

There are several options possible for distributing forcing files that already exist. Note that these scripts do not subset or otherwise modify the data; they simple redistribute and save another copy of the files with the user-defined P/Q/R.

### Option 1: Use a ParFlow Run object
The Shell script `distribute_forcing_run.sh` calls the Python script `distribute_forcing_run.py`. This script is set up to redistribute an existing set of forcing files. Please note that this will overwrite the files that you point to, so please make your own copy of files before redistributing in this way. This script loops through each variable and defines each file timestep. This could be modified to only redistribute only certain variables and/or timesteps, if desired.

### Option 2: Use `read_pfb` and `write_pfb`
The Shell script `distribute_forcing.sh` calls the Python script `distribute_forcing.py`. This script is set up to utilize a SLURM job array to parallelize the distribution of all variables of forcing files. This script reads in the original forcing file and writes out a new version of that file with the user-defined P/Q/R. This script assumes all forcing files to be redistributed are located in the same input directory and it simple cycles through all files present (regardless of variable name). Please ensure the SLURM array index matches the number of files you are redistributing.