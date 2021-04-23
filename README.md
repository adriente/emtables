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
