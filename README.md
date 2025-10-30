# Kazuya's Data

## Description of Files   
### *metadata_base.csv
This file contains basic information about all samples.  
**columns**
`name`: names of samples  
`group_gnd`: 0, 1, 2 , NaN (ground truth. In case the data is not labeled, it will be NaN.)  
`sheet`: 01_FN, 02_VN, 03_FN_P5D2, 04_VN_P5D2, 05_FN_Cilen100, 06_VN_Cilen100,old_data, old_data_unlabeled (This column indicates the folder to which the data originally belongs)
`status`: labeled, unlabeled (whether the ground truth is provided or not)   
### metadata_split.csv 
In this `.csv` file, test and train data are determined. All the columns are the same as `metadata_base.csv', plus another column called 'split'.
`split`: train, test (whether the data was used as test or train)  
### metadata_features.csv 
Includes all the columns in `metadata_split.csv` plus the prediction information and some of the selected extracted features.
`group_pred`: 0, 1, 2 (predicted group)   
`sarcomere_length_mean`: Mean sarcomere length [µm]   
`sarcomere_length_std`: Average sarcomere length [µm]    
`sarcomere_area_ratio`: Ratio of cell mask area occupied by sarcomeres.   
`z_length_mean`: Mean Z-band length [µm]   
`n_zbands`: Number of Z-bands   
`cell_mask_area`: Cell area [µm²]   

## data_info.csv
Find the info for the `.csv` file `data_info.csv` below:    
**Columns**   
`name`: names of samples  
`group_pred`: 0, 1, 2 (predicted group)    
`group_gnd`: 0, 1, 2 , NaN (ground truth. In case the data is not labeled, it will be NaN. )     
`sheet`: 01_FN, 02_VN, 03_FN_P5D2, 04_VN_P5D2, 05_FN_Cilen100, 06_VN_Cilen100,old_data, old_data_unlabeled (This column indicates the folder to which the data originally belongs)   
`sarcomere_length_mean`: Mean sarcomere length [µm]   
`sarcomere_length_std`: Average sarcomere length [µm]    
`sarcomere_area_ratio`: Ratio of cell mask area occupied by sarcomeres.   
`z_length_mean`: Mean Z-band length [µm]   
`n_zbands`: Number of Z-bands   
`cell_mask_area`: Cell area [µm²]   
`status`: labeled, unlabeled (whether the ground truth is provided or not)   
`split`: train, test (whether the data was used as test or train)  

-----
## Project Background
Write about stem cells, heart cells, matureness immatureness? why is it important to classify them into three groups

## Project Roadmap  
Installing requirements.    
raw_folder -> features folder    
using a list of names, we set test and train   
using a list of features, we select features for test and train   
scaling and all   
clustering 
comparing the gnd and reality   
MAYBE YOU WANNA GO INTO SAMPLES ONE BY ONE JUST TO MAKE SURE?  

## Step 0-a: Installation Instructions
### Requirements
You’ll need **Miniconda** (or **Anaconda**) installed on your system.
If you already have **Conda**, you can use it instead of **Miniconda** and replace all `mamba` commands below with `conda`.
  
### Environment Setup
Because of dependency version conflicts, two separate Conda/Miniconda environments were created for this project:  
-`featextract-env`: includes [SarcAsM](https://github.com/danihae/SarcAsM) for feature extraction.    
-`featanalysis-env`: includes [ExKMC](https://github.com/navefr/ExKMC?tab=readme-ov-file) and its related dependencies for the cell grouping process.  

#### 1. Feature Extraction Environment
Write the following commands in your terminal.
```
module load miniconda
mamba create --name featextract-env python=3.12 -y 
mamba activate featextract-env
pip install sarc-asm
```
   
#### 2. Feature Analysis Environment
Write the following commands in your terminal.
```
module load miniconda
mamba create -n featanalysis-env python=3.10 -y
mamba activate featanalysis-env
mamba install -y numpy=1.23 pandas matplotlib scikit-learn
mamba install -y tifffile graphviz python-graphviz cython compilers
pip install ExKMC
```
**Note**: For deactivation of environments, use:   
`
mamba deactivate
`
After creation of the first env, deactivate it and create the next. 
### Using the Environment in VS Code
If you are using VS Code:

1. Open the project folder in VS Code.
2. Make sure the **Python** and **Jupyter** extensions are installed (you can find them in the Extensions tab).
3. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS).
4. Search for “Python: Select Interpreter”.
5. Choose the environment you created (e.g., featextract-env or featanalysis-env).

------------------
## Step 0-b: Setting up Folder Directories and Assigning Test-Train Data  
In this step 

## Step 1: Feature Extraction  


## Step 2: Feature Analysis and Saving Results

## Files
just make everything into one utils file

## Tutorials

## THINGS TO TALK ABOUT   

    
instruction for setting up envs   
.py utils_file   
.csv file for the names and gnd  
.csv file for the names and gnd test and train are also added
.py file for feature extraction   
.py file for grouping them and visualizing 
.csv file for the names and pred

