# Contributing

## Workflow

Direct pushes to `main` are disabled — all changes must go through a pull request.

1. **Open an issue** to discuss a new pipeline, analysis, or bug before writing code.
This will make it easier to keep everyone up to date on what folks are working on so we don't duplicate work.
2. **Create a branch** from `main`:
   ```bash
   git checkout -b your-name/brief-description
   ```
3. **Make your changes.** See the sections below for conventions.
4. **Open a pull request** against `main`.
Use the PR template to describe your changes.
5. **Request a review** from at least one other team member before merging.

## Branch naming

Use the pattern `<yourname>/<topic>`, e.g.:

```
jfcrenshaw/lbg-selection-cuts
```

## Pipeline changes

- Place new pipelines under `configs/pipelines/<name>/` (a `pipeline.yml` and a `config.yml`).
- Add a new run config under `configs/runs/<name>.yml` for any new dataset or run combination.
- Update `docs/pipelines/index.md` if a new pipeline is added.
- If you add new shared reference files, put them in `configs/`.

## Notebook conventions

- Strip outputs before committing (handled by the `nbstripout` pre-commit hook).
- Name notebooks descriptively, e.g. `<topic>_<data_version>.ipynb`.

## Python code

We use [ruff](https://docs.astral.sh/ruff/) for linting and formatting (enforced by pre-commit):

```bash
ruff check --fix .   # lint
ruff format .        # format
```

## Documentation

The docs site is built from the `docs/` directory with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).
To preview locally:

```bash
pip install mkdocs-material
mkdocs serve
```

Updates to `docs/` on `main` are deployed automatically to GitHub Pages via the CI workflow.

## Questions

Post in the LBG topical team Slack channel (`#desc-lbg`) or open a GitHub issue.
