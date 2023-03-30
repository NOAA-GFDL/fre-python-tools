# fre-python-tools
Python-based tools and interfaces to be used by FRE workflows

## Install with miniconda and pip (recommended)
Some prerequisites require miniconda, so the current recommendation is to
install the prerequisites with minconda first, then install fre-python-tools
via pip. This method has the advantage of pip-installing your local changes.

1. Install dependencies

```
conda env create --file environment.yml
```

2. Install fre-python-tools

```
pip install .
```

3. Run tests

```
pip install pytest
pytest
```

## Install with miniconda alone
The miniconda environment.yml file installs the main branch of the
fre-python-tools repository, so if you do not need to install local changes,
the second step above can be omitted. i.e.:

```
conda env create --file environment.yml
```

## How to install with pip alone (not generally recommended)
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
