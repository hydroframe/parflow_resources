#!/bin/bash
#SBATCH --job-name=daily_agg_pf    # create a short name for your job
#SBATCH --output=pf-%A.%a.out # stdout file
#SBATCH --error=pf-%A.%a.err  # stderr file
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=80G        # memory per cpu-core (4G is default)
#SBATCH --time=12:00:00          # total run time limit (HH:MM:SS)
#SBATCH --array=0-363%5        # job array with index values 0, 1, 2, 3, 4 
#SBATCH --mail-type=all          # send email when job begins/ends
#SBATCH --mail-user=<user_email_address>

echo "My SLURM_ARRAY_JOB_ID is $SLURM_ARRAY_JOB_ID."
echo "My SLURM_ARRAY_TASK_ID is $SLURM_ARRAY_TASK_ID"
echo "Executing on the machine:" $(hostname)

module purge
module load parflow-shared

# WY2003 is not a leap year so it has 365 days
# Indexing through 364 would include several hours from Oct 1 2004
# for CONUS2 due to the 6 hour CONUS2 offset.
# Indexing through 363 captures all available days with the offset.
python compute_daily_PF_averages.py
