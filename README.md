## Table of contents
- [Project background]( #background )

# Kazuya's Data
## Project background   <a name="background"></a>
Write about stem cells, heart cells, matureness immatureness? why is it important to classify them into three groups

## Project roadmap  
Installing requirements.    
raw_folder -> features folder    
using a list of names, we set test and train   
using a list of features, we select features for test and train   
scaling and all   
clustering 
comparing the gnd and reality   


### Folders
#### csv_files folder  
This folder contains the metadata used in this project, stored as `.csv` files.  

#### figures folder   
Generated figures and visual results are saved in this folder.

#### dataset folder (not on GitHub)  
This folder contains the raw data.
It includes `.tif` files for the raw images and additional folders named after each sample ID.
The feature-extraction tool used in this project, **SarcAsM**, automatically creates a folder for each sample (named after the sample ID) and stores intermediate outputs such as `cell_mask.tif`, `mbands.tif`, `zbands.tif`, etc.

#### dataset_sarcasm_features folder (not on GitHub)   
This folder contains the extracted features from **SarcAsM**, saved as `.csv` files (one per sample).

#### dataset_abnormal_samples folder (not on GitHub) 
If an error occurs during feature extraction, a `.txt` file with the sample ID is stored here. Each file contains the error message for that sample.

### Codes  

### Figures Folder  

-----

## Description of Files   
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
### `step2_metadata_split.py`   
### `step3_analysis_and_metadata_features.ipynb`  
### `utils.py`  

-----------
-----------
## Step 0-a: Installation instructions
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
## Step 1: Feature extraction   
In this step, data are read from the raw data fodler `dataset`, they go through feature extraction in csv . In this step, the csv file `metadata_base.csv` is used to get the names of the files.
**code file corresponding to this step**: `step1_feature_extraction.py`

## Step 2: Setting test and train 
Test and train data are assigned in this step and the `metadata_split.csv` file is geenrated.
**code file corresponding to this step**: `step2_metadata_split.py`

## Step 3: Feature analysis and saving results
**code file corresponding to this step**: `step3_analysis_and_metadata_features.ipynb`


## References  



