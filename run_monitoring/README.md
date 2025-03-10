# run_monitoring

This directory contains notebooks that assist with monitoring ParFlow run status.

- *check_forcing_files_exist.ipynb*: This Jupyter notebook checks that, given a directory and a time range, all expected forcing files exist within that directory. An additional step checks whether distribution files exist. For both checks, produce a plot to easily diagnose any missing files.
- *check_domain_forcing.ipynb*: This Jupyter notebook checks all timesteps of forcing data against your domain mask. Timesteps with missing forcing data within the domain (unexpected) are printed to be able to investigate further.
- *inspect_fix_files.ipynb*: This Jupyter notebook inspects many of the ParFlow run output files, producing information about min/max values and visual plots. There is code for additional inspections regarding high pressure and low pressure regions. Several cells at the bottom of this notebook provide examples of hand-fixing mannings and slope input files based on these outputs.
- *monitor_run_performance.ipynb*: This Jupyter notebook has functions to evaluate and monitor run performance. It produces plots of the number of solver iterations and provides a way to estimate the amount of runtime required for a run to finish.