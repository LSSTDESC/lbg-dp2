#!/usr/bin/env python3
"""Merge pipeline, run, and site YAML configs into a single ceci input file.

This is needed because the installed ceci version accepts only one pipeline
YAML argument.  The three-file structure (pipeline / run / site) is preserved
in the repo; this script merges them at run time.

Usage
-----
    python scripts/merge_configs.py <pipeline_yaml> <run_yaml> <site_yaml>

Writes
------
    results/<run>/pipeline.yaml   merged config passed to ceci
    results/<run>/config.yaml     copy of the per-stage config file

Prints the path to the merged YAML so callers can do:
    MERGED=$(python scripts/merge_configs.py ...)
    ceci "$MERGED"
"""

import shutil
import sys
from pathlib import Path

import yaml


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    pipeline_yaml, run_yaml, site_yaml = sys.argv[1], sys.argv[2], sys.argv[3]

    merged = {}
    for path in (pipeline_yaml, run_yaml, site_yaml):
        with open(path) as fh:
            data = yaml.safe_load(fh)
            if data:
                merged.update(data)

    # Derive the run directory from output_dir (e.g. results/<run>/outputs ->
    # results/<run>/).  This is where we persist the merged configs.
    output_dir = Path(merged.get("output_dir", "results/output"))
    run_dir = output_dir.parent
    run_dir.mkdir(parents=True, exist_ok=True)

    # Write the merged pipeline config
    merged_path = run_dir / "pipeline.yaml"
    with open(merged_path, "w") as fh:
        yaml.dump(merged, fh, default_flow_style=False, sort_keys=False)

    # Copy the per-stage config alongside it for reference
    stage_config = merged.get("config")
    if stage_config:
        shutil.copy(stage_config, run_dir / "config.yaml")

    print(merged_path)


if __name__ == "__main__":
    main()
