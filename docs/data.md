# Data

We will update this page with paths and descriptions of data sets as we start to use them.

## What lives in the repository

The repo tracks only small reference files:
Large catalogs, maps, and pipeline outputs are **not** tracked in git.
They live on NERSC filesystems.

## Filesystem conventions

- **Inputs** come from paths specified in catalog config files.
- **Outputs** go to `results/<run_name>/outputs`.
- **Logs** go to `results/<run_name>/logs/`.
- **Temporary files** (e.g., jackknife scratch) go to `$PSCRATCH`.

`results/*/` is not tracked in git.
