# lbg-dp2 — Claude Code guidance

## What this repo is

DP2 analyses for the DESC LBG Topical Team, hosted at NERSC.
Repo root on CFS: `/global/cfs/cdirs/lsst/groups/WLSS/LBG/lbg-dp2`.
Framework: [ceci](https://ceci.readthedocs.io) / [TXPipe](https://txpipe.readthedocs.io) — pipelines are DAGs of stages defined in YAML.

## Environment

Activate the shared Python environment with:
```bash
lbg-env   # requires setup_lbg_env.sh sourced in ~/.bashrc.ext or ~/.zshrc.ext
```

The `lbg` command is a shortcut to the repo root.

## Directory layout

```
configs/
├── fiducial_cosmology.yml        # shared ΛCDM reference parameters
├── pipelines/
│   ├── README.md                 # list of all pipelines
│   └── <name>/
│       ├── pipeline.yml          # stage DAG + modules + config pointer
│       └── config.yml            # per-stage hyperparameters
├── runs/
│   ├── README.md                 # list of all runs
│   └── <name>.yml                # inputs, output_dir, log_dir, resume flag
└── sites/
    ├── nersc-interactive.yml     # launcher: mini, max_threads: 128
    └── nersc-batch.yml           # launcher: parsl, Perlmutter CPU, m1727
lbg_stages/                       # custom ceci PipelineStage subclasses
results/                          # pipeline outputs (not tracked in git)
scripts/
├── _common.sh                    # shared arg parsing + cd-to-root logic
├── merge_configs.py              # merges pipeline + run + site YAMLs for ceci
├── run_debug.sh                  # auto-requests debug alloc; 2 nodes
├── run_interactive.sh            # use inside existing salloc
└── run_batch.sh                  # sbatch; 4 nodes, regular queue, m1727
```

## Running a pipeline

The run scripts require `lbg-env` to be activated in the **current shell** so the
environment (PATH, Python) is inherited by the compute node via `salloc`.
Always activate before running any script:

```bash
source /global/common/software/m1727/groups/WLSS/LBG/lbg-env/scripts/setup_lbg_env.sh
lbg-env
```

Then:

```bash
bash scripts/run_debug.sh    <pipeline> <run>   # quick test
bash scripts/run_interactive.sh <pipeline> <run> # inside salloc
sbatch scripts/run_batch.sh  <pipeline> <run>   # production
```

`<pipeline>` = directory name under `configs/pipelines/`.
`<run>` = filename (no `.yml`) under `configs/runs/`.
ceci must be invoked from the repo root (the scripts handle this).

## ceci version notes

The installed ceci version accepts only a **single** pipeline YAML (plus `key=value` overrides).
The run scripts work around this by merging `pipeline.yml`, the run config, and the site config into a temp file before calling ceci.
Use `modules:` (space-separated, top-level key) to import stage modules — this is what registers stage classes with ceci.
`python_paths:` is not needed because ceci adds CWD to `sys.path` automatically.

## Pipeline YAML conventions

**pipeline.yml** skeleton:
```yaml
modules: lbg_stages

config: configs/pipelines/<name>/config.yml

stages:
  - name: SomeStage
  - name: AnotherStage
```

**config.yml** skeleton — one block per stage name, empty `{}` until params are known:
```yaml
SomeStage:
  param1: value

AnotherStage:
  {}
```

**run config** skeleton:
```yaml
resume: False
output_dir: results/<run>/outputs
log_dir: results/<run>/logs
inputs:
  fiducial_cosmology: configs/fiducial_cosmology.yml
pre_script: ""
post_script: ""
```

## Adding a new pipeline checklist

1. `cp -r configs/pipelines/template configs/pipelines/<name>`
2. Edit `pipeline.yml` (stages) and `config.yml` (params).
3. Create `configs/runs/<run>.yml`.
4. Add an entry to `configs/pipelines/README.md` and `configs/runs/README.md`.
5. Update `docs/pipelines.md`.

## Git / contribution conventions

- Branch naming: `<yourname>/<topic>` (e.g. `jfcrenshaw/mock-desi`).
- No direct pushes to `main` — all changes via PR with ≥1 review.
- Open an issue before starting a new pipeline or analysis.
- Strip notebook outputs before committing (`nbstripout` pre-commit hook handles this).
- Linting: `ruff check --fix . && ruff format .` (line length 88, Python 3.11+).

## Slurm / NERSC

- CPU account: `m1727`; GPU account: `m1727_g`.
- Constraint: `cpu` (Perlmutter Milan nodes, 128 cores each).
- Outputs to `results/<run>/outputs`, logs to `results/<run>/logs` — neither tracked in git.
- Big I/O scratch: `$PSCRATCH`; persistent output: `/global/cfs/cdirs/desc-wl/LBG/lbg-dp2/results/`.

## Pipelines in this repo

| Pipeline | Run config(s) | Description |
|---|---|---|
| `reduce_flagship_catalog` | `reduce_flagship_catalog` | Flagship pixel files → positions, magnitudes, DESI selector inputs |
| `mock_desi` | `mock_desi_flagship` | Flagship catalog → DESI selector → LSSTErrorModel → i<25 cut |
