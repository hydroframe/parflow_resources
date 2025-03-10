#!/bin/bash
#SBATCH --job-name=yearly_agg    # create a short name for your job
#SBATCH --output=yearly_agg.out # stdout file
#SBATCH --error=yearly_agg.err  # stderr file
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=100G        # memory per cpu-core (4G is default)
#SBATCH --time=00:30:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=all          # send email when job begins/ends
#SBATCH --mail-user=<user_email_address>

module purge
module load parflow-shared

python compute_yearly_averages.py
