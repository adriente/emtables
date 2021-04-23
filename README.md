# This README needs an update

# EMtables
Useful tables for electron spectro-microscopy. 
- For EDXS : Xray line cross-sections, absorption coefficients at edge energy.
			 This work is mainly based on the library xraylib and the work of David Bote.
- For EELS : This may be necessary. A check of what was already done is necessary.

## Installation


### General unix


First install `xraylib`. 

On mac, you simply do
```
brew install tschoonj/tap/xraylib
```
On other linux system, follow:
https://github.com/tschoonj/xraylib/wiki/Installation-instructions

Then initiate the virtual environnement and install the packages using:
```
pipenv --sites-packages --python=/path/to/python/with/xraylib
pipenv install
pipenv shell
```

### Anaconda
- On ubuntu WSL 18.04

First install anaconda : 
```
 wget https://repo.continuum.io/archive/Anaconda3-2020.11-Linux-x86_64.sh
```
```
bash Anaconda3-2020.11-Linux-x86_64.sh
```
```
conda install -c conda-forge xraylib
```
Then install with pipenv : 
```
cd working_directory
```
```
pipenv --python=/path/to/anaconda3/bin/python --site-packages
pipenv install
```
- Without the Pipfile:
```
pipenv --python=/path/to/anaconda3/bin/python --site-packages
pipenv install -e .
```
- Daily usage once installed : 
Activate the virtual environment using : 
```
pipenv shell
```

## Usage

This a temporary usage but for now it works. 

### For EDXS table

Go to the tables folder and run : 
```
python EDXS_table.py
```
It will print a reduced version of the table (gold only with reduced electron energy). Then you will be prompted if you want to output the full table. To accept press y then enter. 

### For absorption coefficient table

Go to the tables folder and run : 
```
python abscoeff_table.py
```
It will print a reduced version of the table (gold only). Then you will be prompted if you want to output the full table. To accept press y then enter. 
