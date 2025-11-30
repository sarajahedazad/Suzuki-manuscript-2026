# Kazuya's Data
## Table of contents
- [Project overview]( #overview )
- [Project roadmap]( #roadmap )
- [Description of folders](#folders)
- [Description of key files](#files)
- [Installation instructions](#step0)
- [Workflow](#workflow)
    - [Step 1: Feature extraction](#step1)
    - [Step 2: Setting test and train](#step2)
    - [Step 3: Fitting training data and evaluating](#step3)
    - [Step 4: Analyzing results](#step4)
- [References](#references)

## Project overview   <a name="overview"></a>
Human induced pluripotent stem cell-derived cardiomyocytes (hiPSC-CMs) change significantly as they grow. Their internal structure varies across different stages of maturation. In this project, our goal is to group these cells into three categories: low, medium, and high organization, based on structural features extracted from their images.

We used a deep-learning based open-source tool called [SarcAsM](https://github.com/danihae/SarcAsM) to extract detailed structural features from each cell. After feature extraction, we applied K-means clustering to identify three groups in the data. Using the fitted K-means model and the extracted features, we then trained a decision tree to classify new samples into these groups.

This workflow allows us to categorize large sets of hiPSC-CM images according to their level of internal structural organization.

## Project roadmap  <a name="roadmap"></a>   
`Installing the required dependencies`↦`Extracting features`↦`Train and test split`↦`Fitting training data and evaluating`↦`Analyzing results`

## Description of folders <a name="folders"></a> 
### `csv_files` folder  
This folder contains the metadata used in this project, stored as `.csv` files and also some results from test data evaluation.  

### `figures` folder     
Generated visual results are saved in this folder.

### `text_results` folder     
Contains files in `.txt` format from the results of `step3_fit_and_eval.py`. These data, alongside with the information in ` metadata_features.csv `, are used in `step4_analyze_results.py` for analysing results, and in `results_visualization.ipynb` for visualization of results.

### `dataset` folder (not on GitHub)   
This folder contains the raw data.
It includes `.tif` files for the raw images and additional folders named after each sample ID.
The feature-extraction tool used in this project, **SarcAsM**, automatically creates a folder for each sample (named after the sample ID) and stores intermediate outputs such as `cell_mask.tif`, `mbands.tif`, `zbands.tif`, etc.

### `dataset_sarcasm_features` folder
This folder contains the extracted features from **SarcAsM**, saved as `.csv` files (one per sample).

### `dataset_abnormal_samples` folder (not on GitHub) 
If an error occurs during feature extraction, a `.txt` file with the sample ID is stored here. Each file contains the error message for that sample. In case no error happens, this folder will be empty.


## Description of key files <a name="files"></a>    
### ` metadata_base.csv `<a name="metadatabase"></a>    
This file contains basic information about all samples.  
**Columns**:  
- `name`: names of samples  
- `group_gnd`: 0, 1, 2 , NaN (ground truth. In case the data is not labeled, it will be NaN.)  
- `orig_folder`: 01_FN, 02_VN, 03_FN_P5D2, 04_VN_P5D2, 05_FN_Cilen100, 06_VN_Cilen100, old_data, old_data_unlabeled, data_nov (This column indicates the folder to which the data originally belongs)
- `status`: labeled, unlabeled (whether the ground truth is provided or not)   
### ` metadata_split.csv ` <a name="metadatasplit"></a>    
This file includes all columns from `metadata_base.csv`, plus an additional column defining the train/test split.   
**Additional Columns**:
- `split`: train, test (whether the data was used as test or train)  
### ` metadata_features.csv ` <a name="metadatafeats"></a>    
This file extends `metadata_split.csv` by adding prediction results and selected extracted features.  
**Additional Columns**:  
- `group_pred`: 0, 1, 2 (predicted group)   
- `sarcomere_length_mean`: Mean sarcomere length [µm]   
- `sarcomere_length_std`: Average sarcomere length [µm]    
- `sarcomere_area_ratio`: Ratio of cell mask area occupied by sarcomeres.   
- `z_length_mean`: Mean Z-band length [µm]   
- `n_zbands`: Number of Z-bands   
- `cell_mask_area`: Cell area [µm²]

### `PC_train.txt`  
A Principal Component Analysis (PCA) model (with the first 2 components) was fitted on the scaled training features, and the resulting transformed array is saved.
 
### `PC_test.txt`  
After scaling the test features using the train-fitted scaler and then applying the PCA model that is fitted on the training data, the transformed test array is saved.
`PC_train.txt` and `PC_test.txt` are used in visualizing clusters.

### `utils.py`  
Contains helper functions used across different scripts in the project.

### `step1_feature_extraction.py`  
Extracts structural features from the raw .tif images using the SarcAsM pipeline.
This script reads the input dataset, runs feature-extraction for each sample, and saves the resulting feature files. 

### `step2_traintest_split.py`   
Creates a train/test split based on the metadata.
This script loads the base metadata file (`metadata_base.csv`), assigns each sample to the train or test set (following predefined rules), and saves the updated metadata as `metadata_split.csv`.  

### `step3_fit_and_eval.py`  
A `.py` file for fitting the model on the training data, evaluating it on the test data, and saving the results.  
It loads `metadata_split.csv` and the feature files, performs the analysis, and generates outputs such as `metadata_features.csv`, `PC_train.txt`, and `PC_test.txt`.

### `step4_analyze_results.py`  
This script loads the results from the previous steps, including `metadata_features.csv`, `PC_train.txt`, and `PC_test.txt`, and performs analyses such as generating confusion matrices and creating visualizations.

### `results_visualization.ipynb`
This Jupyter notebook is used for visualizing the same results generated in Step 4. It does not save any outputs; it is only used for visualization.

## Installation instructions <a name="step0"></a>    
### Requirements
You’ll need **Miniconda** (or **Anaconda**) installed on your system.
If you already have **Conda** set up, you can use that instead of **Miniconda**. Just replace all `mamba` commands below with `conda`.
  
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
**input needed**:   
- raw `.tif` files from the `dataset` folder (not on GitHub)
**code file corresponding to this step**:   
- `step1_feature_extraction.py`
**generated files**:    
- all features data (`.csv` files) in `dataset_sarcasm_features` folder
- the intermediate SarcAsM outputs (such as `zbands.tif`, `mbands.tif`, `cell_mask.tif`, etc) stored in per-ID subfolders inside `dataset` folder (not on GitHub)

### Step 2: Setting test and train <a name="step2"></a>    
**input needed**:  
- `metadata_base.csv` 
**code file corresponding to this step**:   
- `step2_traintest_split.py`
**generated files**:   
- `metadata_split.csv` (in `csv_files` folder)

### Step 3: Fitting training data and evaluating <a name="step3"></a> 
**input needed**:  
- all features data (`.csv` files) in `dataset_sarcasm_features` folder
- `metadata_split.csv` (in `csv_files` folder)
**code file corresponding to this step**:  
- `step3_fit_and_eval.py`
**generated files**:  
- all data in the `text_results` folder
- `metadata_features.csv` (in `csv_files` folder)

### Step 4: Analyzing results <a name="step4"></a>
**input needed**:   
- raw `.tif` files from the `dataset` folder (not on GitHub)
- the intermediate SarcAsM outputs (`zbands.tif`) stored in per-ID subfolders inside `dataset` folder (not on GitHub)
- the data in `text_results`
- `metadata_features.csv` (in `csv_files` folder)   
**code file corresponding to this step**:  
- `step4_analyze_results.py`  
**generated files**: 
- `cm_test.csv`(in `csv_files` folder)  
- `perclass_test.csv` (in `csv_files` folder)
- `summary_test.csv` (in `csv_files` folder)  
- all files in `figures` folder

### Going through steps
For step 1 use `featextract-env` and for step 2 & step 3 use `featanalysis-env`. **Do not forget to alter the directories in each file based on the directories in your computer.** 

For feature extraction in **step 1**, you need a folder of cardiomyocyte images in `.tif` format.

For running `step 2` (the train–test split), you also need a .csv file similar to [metadata_base.csv](#metadatabase), with at least a column named `name` and another column named `group_gnd`. In our case, we also had a column called `orig_folder`, which we used to decide the train and test samples. You can change this part if you want to use a different method to split the data(like random splot, for example). Just be careful: for the train set you don’t necessarily need the ground truth, but for the test set you do, so only select labeled samples for test.

**Feature extraction**
```
module load miniconda
mamba activate featextract-env
python3 step1_feature_extraction.py
```
**Feature analysis**
```
module load miniconda
mamba activate featanalysis-env
python3 step2_traintest_split.py
python3 step3_fit_and_eval.py
python3 step4_analyze_results.py
```
**Note 1**: The file `results_visualization.ipynb` is the same as `step4_analyze_results.py`, except it does not save any results and is used only for visualization.  
If you would like to open it as a Jupyter notebook in your browser, you may need to install Jupyter Notebook in your conda environment as well:
```
pip install jupyter
```
```
jupyter notebook results_visualization.ipynb
```
**Note 2**: Depending on how the environment is set up, for example the SarcAsM version, the versions of its dependencies, etc, there can be subtle differences in the extracted features between runs.

## References  
- [SarcAsM GitHub](https://github.com/danihae/SarcAsM)
- [ExKMC GitHub](https://github.com/navefr/ExKMC?tab=readme-ov-file)


