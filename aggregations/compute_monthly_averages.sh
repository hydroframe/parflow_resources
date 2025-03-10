#!/bin/bash
#SBATCH --job-name=monthly_agg    # create a short name for your job
#SBATCH --output=%A.%a.out # stdout file
#SBATCH --error=%A.%a.err  # stderr file
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=100G        # memory per cpu-core (4G is default)
#SBATCH --time=1:00:00          # total run time limit (HH:MM:SS)
#SBATCH --array=0-11%4         # job array with index values 0, 1, 2, 3, 4
#SBATCH --mail-type=all          # send email when job begins/ends
#SBATCH --mail-user=<user_email_address>

echo "My SLURM_ARRAY_JOB_ID is $SLURM_ARRAY_JOB_ID."
echo "My SLURM_ARRAY_TASK_ID is $SLURM_ARRAY_TASK_ID"
echo "Executing on the machine:" $(hostname)

module purge
module load parflow-shared

python compute_monthly_averages.py
