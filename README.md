# ShoreFor
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
***
## General Informations

ShoreFor is an equilibrium cross-shore model. The present model is written in Python 3 and based on [Splinter et al. (2014b)](doc/SPLINTER-2014b_A_generalized_equilibrium_model_for_predicting_daily_to_interannual_shoreline_response.pdf).

ShoreFor is based on an equation that contains three parameters that are calibrated/optimized with data: b, c and &phi; (memory decay). These parameters are optimized with Dakota software ([*https://dakota.sandia.gov/*](https://dakota.sandia.gov/)).

The user only needs to modify the configuration file `config_shorefor.yaml`.

The [**examples**](./examples/) directory contains two input files for the Truc Vert (France) beach:

- [`Shoreline_1.5.dat`](./examples/Shoreline_1.5.dat), the survey data;

- [`TrucVert_Forcing.dat`](./examples/TrucVert_Forcing.dat), the forcing data.

## Installation and usage

### Download this repository

For example by running:
```
git clone https://gricad-gitlab.univ-grenoble-alpes.fr/mepels/ShoreFor.git
```

### Set up the environment
#### Option 1: using Anaconda

**Anaconda** can be downloaded freely [here](https://www.anaconda.com/download/). Once installed, open a terminal (for Linux and MacOS; the Anaconda prompt for Windows) and go to the directory where you downloaded this repository. 

Then create a new environment and install the packages:
```
conda create -n shorefor python=3.9.7
conda activate shorefor
conda install -c anaconda pyyaml
conda install anaconda::pandas
conda install conda-forge::matplotlib
conda install anaconda::seaborn
```

Make sure that the environment is activated when you want to use ShoreFor by running
```
conda activate shorefor
```

#### Option 2: using pip

If you don't use **Anaconda** you can install the required packages by running the following command in a terminal:
```
pip install requirements.txt
```

### Dakota

You also need to install Dakota, see [here](https://dakota.sandia.gov/downloads/) and follow the steps for your OS. Tested versions: dakota-6.14 and dakota-6.15.

To check if your installation is complete, you can ask the version:
```
dakota -version
```

### Edit configuration files

The first configuration file to edit is `config_shorefor.yaml`. It handles all the parameters the code needs, and it is organized as follows:
- `STUDY INFO`
    - `study`: the name you want to give to your study
    - `evolution`: 1 if your study is about shoreline, 2 for bars
- `INPUT FILES`
    - `shoreline_file`: path of the shoreline or bar data file; it must contains two columns separated by space(s):
        - first: date in serial date number format
        - second: the shoreline/bar position
    - `waves_file`: path of the wave data; it must contains three columns separated by space(s):
        - first: date in serial date number format
        - second: significant height values in m
        - third: peak period values in s
- `OPTIMIZATION`
    - `dakota`: 1 if you want to use Dakota, 2 if you already know the parameters or if you want to optimize manually
    - `b`: value of parameter b
    - `c`: value of parameter c
    - `phi`: value of parameter phi
    - `dakota_params`: if you want to use Dakota, change here the min and max values for each parameters
- `BEGIN AND END TIMES`
    - `calibration`: modify the initial `time_initial` and final `time_final` dates for the calibration of parameters
    - `future`: set `extrapolate` to 1 if you want to make forecast, 2 if you don't. In the first case, change the initial `begin_future_time` and final `final_future_time` dates for the forecast

If ou want to use Dakota, you need to edit the .in and .sh files:
- `dakota_pstudy.in`: in this file you can modify the method of optimization in Dakota, the names of files and work directory or the name of the response function on which the optimization is realized. However :warning: DO NOT TOUCH the `variables` part :warning: It is automatically handled by the Python script.
- `text_book_bash.sh`: bash script used by Dakota to run the optimization script `objective_function.py` and write the results in `results.txt` in every work directory, one per set of parameters tested 

### Run

Finally run:
```
python shorefor.py
```

### :warning: Errors

On MacOS, if you tried to install Dakota from the source and you get an error of this type: ```dyld[]: Library not loaded```, try to run: ```brew update```.

If then you get an error of this type: ```dyld[]: missing symbol called```, I can't help you. Just download the binaries, it worked fine for me.

## Outputs
- For a simple calibration without extrapolation, the model will plot a figure with two graphs. The top one shows the Dean parameter for the survey series (black line) with the equilibrium Dean parameter (red dashes). The bottom one shows the computed shoreline position (black line) and the survey data (colored dots).
- If an extrapolation is required, a third graph is plotted, with the future evolution of the shoreline.
- Dakota will generate two outputs *dakota_rst* and *dakota_tabular.dat* that contains all the tested parameters. It will also generate a directory *workdir.runnumber* for every run.
- ShoreFor results are printed in *results_shorefor.csv*.

## ToDo
- [ ] Improve the size of figures
- [ ] Check the direction of shoreline position problem
- [ ] Add different dates formats
