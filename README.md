# This README needs an update

# EMtables
Useful tables for electron spectro-microscopy. 
- For EDXS : Xray line cross-sections, absorption coefficients at edge energy.
			 This work is mainly based on the library xraylib and the work of David Bote.
- For EELS : This may be necessary. A check of what was already done is necessary.

## Installation

On ubuntu WSL 18.04

First install anaconda : 
```
 wget https://repo.continuum.io/archive/Anaconda3-2020.11-Linux-x86_64.sh
```
```
bash Anaconda3-2020.11-Linux-x86_64.sh
```

Then install with pipenv : 
```
cd working_directory
```
```
pipenv install --python=/path/to/anaconda3/bin/python --site-packages -e .
```
I did in two steps :
```
pipenv --python=/path/to/anaconda3/bin/python --site-packages
pipenv install -e .
```
But I don't think it makes sense. 
