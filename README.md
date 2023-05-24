# fre-python-tools
Python-based tools and interfaces to be used by FRE workflows

## Install prerequisites with conda and fre-python-tools with pip

Many prerequisites for `fre-python-tools` are available via conda, so
creating a conda environment and pip-installing the package is preferred for
development purposes.

1. Create conda environment that contains all prerequisites
```
conda env create --file environment.yml
```

2. Activate conda environment

```
conda activate fre-python-tools-dev
```

3. Run tests and evaluate outcome

At this point, fre-python-tools is not installed in your environment.
You can run tests on the checked-out code with `python -m pytest`
(compared to `pytest` which does NOT add the current directory to `sys.path`.)

```
python -m pytest
```

There should be no errors. You may get a harmless
warning regarding the deprecation of `sre_constants` within the `metomi.isodatetime`
package.

4. Install fre-python-tools into conda environment
```
pip install .
```

You can run tests on the installed code with:
```
pytest
```

## Install fre-python-tools with conda

`fre-python-tools` is available on NOAA-GFDL's anaconda channel.
To create a new conda environment containing `fre-python-tools`:


```
conda create --name fre-python-tools fre-python-tools --channel=noaa-gfdl
```

Then, activate the environment to bring fre-python-tools libraries and scripts into your PATH.

```
conda activate fre-python-tools
```
