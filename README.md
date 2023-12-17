# BE 562 Final Project: 
### Predicting the Brain’s Internally-Generated Spatial Representations Using Tree Augmented Bayesian Networks

## Getting Started

### Prerequisites

The things you need before installing the software.

* Python 3.8.10 or later
* git bash
* vscode (or any text editor)

### Installation

To load the project, clone the git repository onto your PC.

```
git clone https://github.com/chrisdchan/BE_562_EEG.git
```

Once the repo is cloned onto your PC, it is recomended to create a python virtual environment. This can be done in git bash using the following commands

```
python -m venv env
```

To activate the virtual environment, run:  
On Mac:
```
source env/bin/activate
```
In Windows CMD:
```
 env/Scripts/activate.bat
```
In Windows Powershell:
```
 env/Scripts/Activate.ps1
```
In Git BASH:
```
source env/Scripts/activate
```

Once activeted, download the required dependencies.

```
pip install -r requirements.txt
```

## Usage

To run code that calculates the test accuracies, run "test_model.ipynb". The notebook will calculate the test accuracies described in the report and is commented for ease of undeRstanding.  

Model parameters are already claculated and stored in the "dependencies" folder. To run the code that calculates these, run:
```
get_I_matrix.py
Kruskal.py
learn_params.py
```
NOTE: The script "get_I_matrix.py" utilized multiprocessing to calculte the I matrix. Since it utilizes integration, it can take a long time to run (~ 2 hours with multiprocessing). DO NOT RECCOMEND TO RUN

## Important Notes

Although the MATLAB scriptd for EEG preprcessing are given, we did not include the raw data due to the shear amount of data. The raw files can be found [here.](https://figshare.com/articles/dataset/tracking_task_dataset/13933058/1) The preprocessed data is given in the repo.


## Acknowledgments

Created by Massinissa Bosli, Chris Chan, Teertha Ayanji, & Vatsal Shrivastava for BE 562
