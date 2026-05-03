# Getting Started

## Environment setup

First setup the `lbg-env` tool by adding the following to your `~/.bashrc.ext` (or `~/.zshrc.ext`):

```bash
source /global/common/software/m1727/groups/WLSS/LBG/lbg-env/scripts/setup_lbg_env.sh
```

Then either start a new shell or re-source your `~/.bashrc.ext`/`~/.zshrc.ext` to pick up the change.
You now have access to the `lbg-env` tool.

Typing `lbg` in the terminal now provides a shortcut to the LBG project directory, and typing `lbg-env` will activate the latest shared LBG TT python environment.
You can type `lbg-env help` to see other options provided by this tool, or you can see the README in the [lbg-env GitHub repo](https://github.com/LSSTDESC/lbg-env).

## Running a pipeline

The simplest way to run a pipeline is with `run_debug.sh`, which requests a
short debug allocation automatically and runs the pipeline inside it:

```bash
bash scripts/run_debug.sh <pipeline> <run>
```

where `<pipeline>` is the name of a directory under `configs/pipelines/` and
`<run>` is the name of a file (without the `.yml` extension) under `configs/runs/`.

See [Pipelines](pipelines/index.md) for a full description of each pipeline and instructions
for creating run configs.

## Contributing

To contribute to this project, see the instructions in [Contributing](contributing.md)
