# fre-python-tools
Python-based tools and interfaces to be used by FRE workflows

## How to install with pip
Most of fre-python-tools can be installed with pip and setuptools,
but some tools require conda. pip-installing is faster and
more convenient for purposes where the conda prerequisites are not needed.

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

## How to install with conda
Currently, this method has the disadvantage of using the main branch of the
fre-python-tools repository. From an already installed miniconda installation,
create the conda environment with:

```
conda env create --file environment.yml
```
