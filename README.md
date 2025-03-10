# parflow_resources
This repo contains scripts, helper functions, and assorted tools that were used when running a ParFlow model on the entire CONUS2 domain. Some of these scripts have been adapted to use a computing cluster, such as Princeton's Tiger3 cluster, while others are more general. Our goal is to provide these as resources that may be adapted for other large-scale ParFlow runs.

Please feel free to contribute your own scripts/workflows that faciliate doing research with ParFlow! To contribute, clone this repo and create a feature branch for your contributions. Create a Pull Request for that branch in order to merge them back into the main branch.

### Repository Contents:
- **aggregations/**: Scripts for aggregating hourly ParFlow output to daily, monthly, and yearly files.
- **animations/**: Notebook for creating an mp4 animation from daily ParFlow output files.
- **distribute_forcing/**: Scripts for re-distributing input forcing files.
- **file_transfers/**: Example script for batch transferring files via Globus CLI.
- **run_monitoring/**: Notebooks for monitoring the status of a ParFlow run.
