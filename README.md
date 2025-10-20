# Kazuya-s-Data

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

## Installation Instructions
What do you need? miniconda   
how do you install that?  
How do you setup the env? how to do you install requirements?

## Files
just make everything into one utils file

## Tutorials

