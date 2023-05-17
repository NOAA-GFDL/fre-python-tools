# fre-python-tools
Python-based tools and interfaces to be used by FRE workflows

_______________________________________________________________________________________
_______________________________________________________________________________________
## miniconda installation

Many prerequisites for `fre-python-tools` are available via miniconda. Because of this
creating a conda environment and pip-installing the package is preferred for
development, as the installation step will respect any local changes you've made. 

1. Create conda environment and install dependencies
Create the fre-python-tools conda environment using the packages specified in
`environment.yml`

```
conda env create --file environment.yml
```

2. Activate conda environment and install fre-python-tools

```
conda activate fre-python-tools
```

3. Run tests and evaluate outcome

tests can run with

```
python -m pytest tests/
```

There should be no errors if installation proceeded correctly. You may get a harmless
warning regarding the deprecation of `sre_constants` within the `metomi.isodatetime`
package.

_______________________________________________________________________________________
_______________________________________________________________________________________
## miniconda installation via gfdl conda-channel (currently chris.blanton channel)

one-line installation from Christopher Blanton's conda channel:

```
conda install fre-python-tools --channel=chris.blanton
```

In the future, this will be done through a gfdl conda channel:

```
conda install fre-python-tools --channel=gfdl
```

Make your changes to the relevant places in environment.yml, meta.yaml, setup.cfg, and 
publish the recipe to the conda channel if desired (requires conda-build)

```
conda build . 
```

____________________________________________________________________________________
_______________________________________________________________________________________

## Install with pip alone (not generally recommended)
This method will not install all prerequisites, so is not recommended except for
purposes where the conda prerequisites are not needed.

1. Create virtual python environment

```
python3 -m venv /path/to/your/install
```

2. Activate the environment

```
source /path/to/your/install/bin/activate
```

3. Upgrade pip and setuptools

```
pip install --upgrade pip setuptools
```

4. Install fre-python-tools and dependencies

```
pip install .
```

5. Run tests

```
pip install pytest
pytest
```


