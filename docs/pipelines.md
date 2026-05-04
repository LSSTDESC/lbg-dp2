# Pipelines

Our pipelines use the [TXPipe](https://txpipe.readthedocs.io) / [ceci](https://ceci.readthedocs.io) framework.
Each pipeline is a YAML file that declares a directed acyclic graph (DAG) of stages; ceci resolves dependencies and runs them in order.

## Directory structure

```
configs/
├── fiducial_cosmology.yml      # shared ΛCDM reference parameters
├── pipelines/
│   └── template/
│       ├── pipeline.yml        # stage definitions
│       └── config.yml          # stage hyperparameters
├── runs/
│   └── template.yml            # starting point for a new run
└── sites/
    ├── nersc-interactive.yml   # launcher settings for interactive alloc
    └── nersc-batch.yml         # launcher settings for sbatch jobs
```

A pipeline run is configured by two kinds of file:

- one or more **pipeline** directories under `configs/pipelines/`, each defining a stage DAG and per-stage parameters, and
- a **run** file under `configs/runs/` that names which pipeline(s) to run and specifies inputs, output locations, and run options.

The pipeline configs are kept agnostic to the specific catalogs being analysed, so the same pipeline can be rerun on different inputs simply by writing a new run config.
A run config can also compose multiple pipelines by listing them under the `pipelines:` key — their stages, modules, and per-stage configs are merged automatically.

## Pipeline configs

[List of pipelines](../configs/pipelines/README.md)

Each file in `configs/pipelines/` defines one pipeline:

```yaml
# Template pipeline — copy this directory to pipelines/<name>/

# Space-separated list of modules to import so ceci can find the stage classes.
# Default is just our lbg_stages module, but another common one is txpipe
modules: lbg_stages

# Config file for this pipeline
config: configs/pipelines/template/config.yml

# Define all the stages.
# Ceci will use their inputs/outputs to figure out in which order to run them.
stages:
  - name: Stage1
  - name: Stage2
  # Add more stages here
```

## Run configs

[List of runs](../configs/runs/README.md)

Each file in `configs/runs/` defines one run:

```yaml
# Template run config — copy to runs/<name>.yml and fill in the details.

resume: False  # Whether to re-run stages whose outputs already exist

# Pipeline(s) to run. Use a single name or a list.
pipelines: <pipeline-name>
# pipelines:
#   - pipeline1
#   - pipeline2

# Location where outputs are saved - REPLACE <run> with the name of the run!
output_dir: results/<run>/outputs
log_dir: results/<run>/logs

# Inputs required to run the stages in the pipeline
inputs:
  fiducial_cosmology: configs/fiducial_cosmology.yml
  # Add more inputs here

# These will be run before and after the pipeline respectively
pre_script: ""
post_script: ""
```

## Running a pipeline

Three run scripts are provided in `scripts/`.
Each takes a run name as its first argument; the pipeline(s) to execute are read from the `pipelines:` key in the run config.
Any additional arguments are forwarded directly to `ceci`.

**Quick test** (requests a 2-node debug allocation automatically):

```bash
bash scripts/run_debug.sh <run> [ceci-args...]
```

**Interactive** (use when you already have an `salloc` allocation):

```bash
bash scripts/run_interactive.sh <run> [ceci-args...]
```

**Batch job** (queues a Slurm job; you do not need to stay logged in):

```bash
sbatch scripts/run_batch.sh <run> [ceci-args...]
```

In all cases `<run>` is the name of a `.yml` file (without the extension) under `configs/runs/`.

## Adding a new pipeline

1. Copy the template directory and edit the stages and config:

    ```bash
    cp -r configs/pipelines/template configs/pipelines/<pipeline_name>
    # edit configs/pipelines/<pipeline_name>/pipeline.yml and config.yml
    ```

2. Add an entry to the [list of pipelines](../configs/pipelines/README.md) that documents the pipeline, including the science intent.

## Adding a new run

1. Choose a descriptive run name.
Something like `<pipeline>_<catalog>` is a good option, e.g. `clustering_dp2_24p5`.

2. Copy the run template and fill in the pipeline(s), inputs, and output paths:

    ```bash
    cp configs/runs/template.yml configs/runs/<run_name>.yml
    # edit pipelines:, output_dir, log_dir, and inputs:
    ```

3. Add an entry to the [list of runs](../configs/runs/README.md) that documents the run, including inputs, software versions, and science intent.
