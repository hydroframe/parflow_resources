#!/bin/bash
#SBATCH --job-name=dist_forcing   # create a short name for your job
#SBATCH --output=%A.%a.out # stdout file
#SBATCH --error=%A.%a.err  # stderr file
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=8G        # memory per cpu-core (4G is default)
#SBATCH --time=12:00:00          # total run time limit (HH:MM:SS)
#SBATCH --array=0-2927%10         # job array with index values 0, 1, 2, 3, 4
#SBATCH --mail-type=all          # send email on job start, end and fault
#SBATCH --mail-user=<user_email_address>

module purge
module load parflow-shared

python distribute_forcing.py
