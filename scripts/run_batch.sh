#!/bin/bash
# Submit a pipeline as a Slurm batch job.
# Use this for full-scale production runs. Slurm queues the job and runs it
# when nodes are available; you do not need to stay logged in.
#
# Usage:
#   sbatch scripts/run_batch.sh <pipeline> <run>
#
# Adjust the #SBATCH options below before submitting.

# Project account to charge.
#SBATCH -A m1727

# Request CPU nodes on Perlmutter.
#SBATCH -C cpu

# Queue to submit to. Options: debug (fast, ≤30 min), regular, premium, low.
#SBATCH -q regular

# Maximum wall-clock time. The job is killed if it runs longer than this.
#SBATCH -t 4:00:00

# Number of compute nodes (each has 128 cores on Perlmutter).
#SBATCH -N 4

# Give each task exclusive use of all cores and memory on its node.
#SBATCH -c 128
#SBATCH --mem=0

# Log files. %j is replaced with the Slurm job ID.
#SBATCH -o outputs/logs/slurm-%j.out
#SBATCH -e outputs/logs/slurm-%j.err
#SBATCH --open-mode=append

# shellcheck source=_common.sh
source "$(dirname "$0")/_common.sh"

MERGED=$(python3 scripts/merge_configs.py "$PIPELINE_YAML" "$RUN_YAML" configs/sites/nersc-batch.yml)
ceci "$MERGED"
