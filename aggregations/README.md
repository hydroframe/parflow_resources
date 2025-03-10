# aggregations

These scripts handle various levels of aggregations for ParFlow/CLM outputs. These scripts are set up to be run in parallel on a cluster via SLURM, though modifications could be made to run in a single process with a for-loop instead.

The monthly aggregation requires daily files to exist and the annual aggregation requires monthly files to exist. All indexing is relative to a Water Year (October 1 - September 30).