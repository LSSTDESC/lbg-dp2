#!/bin/bash
# Request a short debug allocation and immediately run a pipeline inside it.
# Use this for quick tests during development. The debug queue is high priority
# but limited to 30 minutes and 2 nodes.
#
# Usage (run from a login node — no salloc needed beforehand):
#   bash scripts/run_debug.sh <run> [ceci-args...]

# shellcheck source=_common.sh
source "$(dirname "$0")/_common.sh"

# salloc reserves the nodes and immediately runs run_interactive.sh inside the
# allocation, releasing the nodes automatically when it finishes.
salloc \
    --nodes 2 \
    --time 00:30:00 \
    --account m1727 \
    --qos debug \
    --constraint cpu \
    bash scripts/run_interactive.sh "$RUN" "${@:2}"
