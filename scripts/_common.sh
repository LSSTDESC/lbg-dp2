# _common.sh — sourced by the run_*.sh scripts. Do not execute this file directly.
#
# Requires lbg-env to be configured in ~/.bashrc.ext or ~/.zshrc.ext (see README).

# Fail immediately on errors, unset variables, or broken pipes.
set -euo pipefail

# Use the calling script's name in error messages rather than "_common.sh".
_SCRIPT=$(basename "${BASH_SOURCE[1]}")

# Two arguments: pipeline name and run name.
PIPELINE=${1:?Usage: $_SCRIPT <pipeline> <run>}
RUN=${2:?Usage: $_SCRIPT <pipeline> <run>}

# ceci must be run from the repo root so that relative paths in the pipeline
# YAML files resolve correctly.
cd "$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)/.."

PIPELINE_YAML=configs/pipelines/$PIPELINE/pipeline.yml
RUN_YAML=configs/runs/$RUN.yml

[[ -f "$PIPELINE_YAML" ]] || { echo "$_SCRIPT: pipeline config not found: $PIPELINE_YAML" >&2; exit 1; }
[[ -f "$RUN_YAML" ]]      || { echo "$_SCRIPT: run config not found: $RUN_YAML" >&2; exit 1; }
