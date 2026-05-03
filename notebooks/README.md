# Notebooks

## Notebook descriptions

-


## Creating a new notebook

### Naming convention

Use descriptive names that indicate the data version and topic, such as `<topic>_<data_version>.ipynb`.
For example,

```
notebooks/lbg_selection_dp2_mocks_v1.ipynb
notebooks/angular_power_spectrum_dp2_23p5.ipynb
```

If you create a number of notebooks to explore results of a specific run you should create a subdirectory to collect those notebooks.


### Adding a description

Make sure you add a brief description to the list at the top of the document.


### Data paths

Notebooks should read data using absolute NERSC paths or the `$LBG_DIR` environment variable.
Do not hardcode `/global/homes/...` paths that only work for one user.


### Clearing outputs

A pre-commit hook strips cell outputs before committing to git.
This ensures the git history does not get too large by including rendered images or data.