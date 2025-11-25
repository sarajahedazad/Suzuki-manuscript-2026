# Kazuya's Data
## Table of contents
- [Project background]( #background )
- [Project roadmap]( #roadmap )
- [Description of folders](#folders)
- [Description of files](#files)
- [Installation instructions](#step0)
- [Workflow](#workflow)
    - [Step 1: Feature extraction](#step1)
    - [Step 2: Setting test and train](#step2)
    - [Step 3: Feature analysis and saving results](#step3)
- [Reproducing the results](#reproduce)
- [References](#references)

## Project background   <a name="background"></a>
Write about stem cells, heart cells, matureness immatureness? why it is important to classify them into three groups

## Project roadmap  <a name="roadmap"></a> 
Installing requirements.    
raw_folder -> features folder    
using a list of names, we set test and train   
using a list of features, we select features for test and train   
scaling and all   
clustering 
comparing the gnd and reality   

## Description of folders <a name="folders"></a> 
### csv_files folder  
This folder contains the metadata used in this project, stored as `.csv` files.  

### Figures folder   
Generated figures and visual results are saved in this folder.

### dataset folder (not on GitHub)  
This folder contains the raw data.
It includes `.tif` files for the raw images and additional folders named after each sample ID.
The feature-extraction tool used in this project, **SarcAsM**, automatically creates a folder for each sample (named after the sample ID) and stores intermediate outputs such as `cell_mask.tif`, `mbands.tif`, `zbands.tif`, etc.

### dataset_sarcasm_features folder (not on GitHub)   
This folder contains the extracted features from **SarcAsM**, saved as `.csv` files (one per sample).

### dataset_abnormal_samples folder (not on GitHub) 
If an error occurs during feature extraction, a `.txt` file with the sample ID is stored here. Each file contains the error message for that sample.  


## Description of key files <a name="files"></a>    
### ` metadata_base.csv `
This file contains basic information about all samples.  
**Columns**:  
- `name`: names of samples  
- `group_gnd`: 0, 1, 2 , NaN (ground truth. In case the data is not labeled, it will be NaN.)  
- `orig_folder`: 01_FN, 02_VN, 03_FN_P5D2, 04_VN_P5D2, 05_FN_Cilen100, 06_VN_Cilen100, old_data, old_data_unlabeled, data_nov (This column indicates the folder to which the data originally belongs)
- `status`: labeled, unlabeled (whether the ground truth is provided or not)   
### ` metadata_split.csv `
This file includes all columns from `metadata_base.csv`, plus an additional column defining the train/test split.   
**Additional Columns**:
- `split`: train, test (whether the data was used as test or train)  
### ` metadata_features.csv `
This file extends `metadata_split.csv` by adding prediction results and selected extracted features.  
**Additional Columns**:  
- `group_pred`: 0, 1, 2 (predicted group)   
- `sarcomere_length_mean`: Mean sarcomere length [µm]   
- `sarcomere_length_std`: Average sarcomere length [µm]    
- `sarcomere_area_ratio`: Ratio of cell mask area occupied by sarcomeres.   
- `z_length_mean`: Mean Z-band length [µm]   
- `n_zbands`: Number of Z-bands   
- `cell_mask_area`: Cell area [µm²]

### `step1_feature_extraction.py`  
Extracts structural features from the raw .tif images using the SarcAsM pipeline.
This script reads the input dataset, runs feature-extraction for each sample, and saves the resulting feature files.   
### `step2_metadata_split.py`   
Creates a train/test split based on the metadata.
This script loads the base metadata file (`metadata_base.csv`), assigns each sample to the train or test set (following predefined rules), and saves the updated metadata as `metadata_split.csv`.  
### `step3_analysis_and_metadata_features.ipynb`  
A Jupyter notebook for analyzing the extracted features and generating the final results.
It loads `metadata_split.csv` and the feature files, performs the analysis, creates visualizations, and saves outputs such as `metadata_features.csv` and various figures. 
### `utils.py`  
Contains helper functions used across different scripts in the project.

## Installation instructions <a name="step0"></a>    
### Requirements
You’ll need **Miniconda** (or **Anaconda**) installed on your system.
If you already have **Conda**, you can use it instead of **Miniconda** and replace all `mamba` commands below with `conda`.
  
### Environment setup
Because of dependency version conflicts, two separate Conda/Miniconda environments were created for this project:  
-`featextract-env`: includes [SarcAsM](https://github.com/danihae/SarcAsM) for feature extraction.    
-`featanalysis-env`: includes [ExKMC](https://github.com/navefr/ExKMC?tab=readme-ov-file) and its related dependencies for the cell grouping process.  

#### 1. Feature extraction environment
Write the following commands in your terminal.
```
module load miniconda
mamba create --name featextract-env python=3.12 -y 
mamba activate featextract-env
pip install sarc-asm   
mamba install -y imagecodecs   
mamba install numpy=2.2 -y   
```
   
#### 2. Feature analysis environment
Write the following commands in your terminal.
```
module load miniconda
mamba create -n featanalysis-env python=3.10 -y
mamba activate featanalysis-env
mamba install -y numpy=1.23 pandas matplotlib scikit-learn
mamba install -y tifffile graphviz python-graphviz cython compilers
pip install ExKMC --no-build-isolation
```
**Note**: For deactivation of environments, use:   
`
mamba deactivate
`
After creation of the first env, deactivate it and create the next. 
### Using the environment in VS code
If you are using VS Code:

1. Open the project folder in VS Code.
2. Make sure the **Python** and **Jupyter** extensions are installed (you can find them in the Extensions tab).
3. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS).
4. Search for “Python: Select Interpreter”.
5. Choose the environment you created (e.g., featextract-env or featanalysis-env).

------------------
## Workflow
### Step 1: Feature extraction   <a name="step1"></a>    
In this step, data are read from the raw data fodler `dataset`, they go through feature extraction in csv . In this step, the csv file `metadata_base.csv` is used to get the names of the files.
**code file corresponding to this step**: `step1_feature_extraction.py`

### Step 2: Setting test and train <a name="step2"></a>    
Test and train data are assigned in this step and the `metadata_split.csv` file is geenrated.
**code file corresponding to this step**: `step2_metadata_split.py`

### Step 3: Feature analysis and saving results <a name="step3"></a>    
**code file corresponding to this step**: `step3_analysis_and_metadata_features.ipynb`

## Reproducing the results <a name="reproduce"></a> 

## References  



