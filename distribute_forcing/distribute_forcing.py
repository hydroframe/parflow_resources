"""Distribute hourly forcing files to a different P/Q/R"""
import os
import glob
from parflow.tools.io import read_pfb, write_pfb

input_dir = 'path/to/original/forcing/files'
output_dir = 'path/to/save/redistributed/files'

# Set desired P/Q/R
p = 70
q = 48
r = 1

idx = int(os.environ["SLURM_ARRAY_TASK_ID"])

file_list = sorted(glob.glob(f'{input_dir}/*.pfb'))
file_name = file_list[idx].split('/')[-1]

f = read_pfb(file_list[idx])
write_pfb(f'{output_dir}/{file_name}', f, p=p, q=q, r=r, dist=True)
