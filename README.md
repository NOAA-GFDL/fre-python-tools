# fre-python-tools
Python-based tools and interfaces to be used by FRE workflows

_______________________________________________________________________________________
_______________________________________________________________________________________
## FOR DEVELOPMENT: miniconda/pip installation

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
pip install .
```

3. Run tests and evaluate outcome

tests can run with

```
pytest
```

There should be no errors if installation proceeded correctly. You may get a harmless
warning regarding the deprecation of `sre_constants` within the `metomi.isodatetime`
package.

_______________________________________________________________________________________
_______________________________________________________________________________________
## FOR USERS: miniconda installation via gfdl-channel (currently chris.blanton channel)

one-line installation from Christopher Blanton's conda channel:

```
conda install fre-python-tools --channel=chris.blanton
```

In the future, this will be done through a gfdl conda channel:

```
conda install fre-python-tools --channel=gfdl
```

_______________________________________________________________________________________
_______________________________________________________________________________________
## For Developers Maintaining fre-python-tools package on gfdl conda channel


Make your changes to the relevant places in environment.yml, meta.yaml, setup.cfg, and 
publish the recipe to the conda channel

```
conda build . 
```
