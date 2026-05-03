# DP2 analyses of the DESC LBG TT

Repo for sharing code related to the LBG TT's DP2 analyses

Location on NERSC: `/global/cfs/cdirs/lsst/groups/WLSS/LBG/lbg-dp2`.

## Setup:

First setup the `lbg-env` tool by adding the following to your `~/.bashrc.ext` (or `~/.zshrc.ext`):

```bash
source /global/common/software/m1727/groups/WLSS/LBG/lbg-env/scripts/setup_lbg_env.sh
```

Then either start a new shell or re-source your `~/.bashrc.ext`/`~/.zshrc.ext` to pick up the change.
You now have access to the `lbg-env` tool.

Typing `lbg` in the terminal now provides a shortcut to the LBG project directory, and typing `lbg-env` will activate the latest shared LBG TT python environment.
You can type `lbg-env help` to see other options provided by this tool, or you can see the README in the [lbg-env GitHub repo](https://github.com/LSSTDESC/lbg-env).

## Running the pipelines

Here's an example of how you might run a pipeline in an interactive debug node.
After logging onto NERSC, from the root of the LBG DP2 repo, run
```bash
bash scripts/run_debug.sh <pipeline> <run>
```

See the [Pipelines](docs/pipelines/index.md) doc for the full description of pipelines, run configs, and the available run scripts.
