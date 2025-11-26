'''------------Importing modules-----------'''
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import Normalizer, StandardScaler
from collections import Counter
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import tifffile
from utils import get_selectedfeats_sarcasm, predict_classes_train, predict_classes_test
from utils import get_loworg_sarcasm, plot_clusters, plot_pca_matches
from utils import evaluate_from_confusion, get_filenames_fromfolder
from utils import samples_by_label_pair
from utils import plot_gndvspred, pick_random_per_pair

'''----------Setting up parameters-----------'''
SEED = 1
split_loworg = True        # whether to set aside low-organization samples during clustering
reverse = False            # Relabel clusters by mean PC1: lowest→0 (or highest→0 if reverse=True)

np.random.seed(SEED)

# Selected features used for clustering
include_lst = ['sarcomere_area_ratio', 'z_length_mean', 'n_zbands']

'''------Setting up directories------------'''
dataset_parent_dir = '/projectnb/lejlab2/Sara/Second Project/kazuyas-data-project'
csvfiles_parent_dir = ''
figures_parent_dir = ''
textresults_parent_dir = ''

# Raw data folder
raw_folder_name = 'dataset'
raw_folder_dir = os.path.join(dataset_parent_dir, raw_folder_name)

# Folder with per-sample sarcasm feature files
sarcasm_features_folder_name = f'{raw_folder_name}_sarcasm_features'
sarcasm_features_dir = os.path.join(dataset_parent_dir, sarcasm_features_folder_name)

# Count available samples based on feature files
print("Total number of data samples is:",
      len(get_filenames_fromfolder(sarcasm_features_dir, file_format="_features.csv")))

# Folder for CSV metadata files
csvfiles_folder_name = 'csv_files'
csvfiles_folder_dir = os.path.join(csvfiles_parent_dir, csvfiles_folder_name)

# Paths to metadata CSV files
metadata_split_csv_dir = os.path.join(csvfiles_folder_dir, 'metadata_split.csv')
metadata_features_csv_dir  = os.path.join(csvfiles_folder_dir, 'metadata_features.csv')  # will be created later

# Folder for figures
figures_folder_name = 'figures'
figures_folder_dir = os.path.join(figures_parent_dir, figures_folder_name)
os.makedirs( figures_folder_dir, exist_ok = True)

# Folder for text results
textresults_folder_name = 'text_results'
textresults_folder_dir = os.path.join(textresults_parent_dir, textresults_folder_name)
os.makedirs( textresults_folder_dir, exist_ok = True)

'''------Setting up test and train------------'''
# Load train/test split metadata
df = pd.read_csv(metadata_split_csv_dir)

# Separate train and test samples
df_train = df[df["split"] == "train"].copy()
df_test  = df[df["split"] == "test"].copy()

# Train set: names + low-org indices
# (low-org indices = samples with n_mbands <= threshold; default thresh=0 but can be changed)
train_names = df_train['name'].to_list()
_, train_idxs_loworg_sarcasm = get_loworg_sarcasm(train_names, sarcasm_features_dir)

# Test set: names + ground-truth labels + low-org indices
test_names  = df_test['name'].to_list()
test_labels = df_test['group_gnd'].to_list()
_, test_idxs_loworg_sarcasm = get_loworg_sarcasm(test_names, sarcasm_features_dir)

# All samples: for global low-org identification
allsamples_names = df['name'].to_list()
_, allsamples_idxs_loworg_sarcasm = get_loworg_sarcasm(allsamples_names, sarcasm_features_dir)

'''---------Fitting train-----------'''
# Train: selected features
train_features = get_selectedfeats_sarcasm(train_names, sarcasm_features_dir,
                                           raw_folder_dir, include_lst)

# Scale train features
scaler = StandardScaler()
train_features_scaled = scaler.fit_transform(train_features)

# PCA on scaled train features
pca = PCA(n_components=2)
train_features_pca = pca.fit_transform(train_features_scaled)

# Cluster + label train samples
train_pred, kmeans, tree = predict_classes_train(
    train_features_scaled, train_features_pca,
    random_state=SEED, split_loworg=split_loworg,
    idxs_loworg=train_idxs_loworg_sarcasm, reverse=reverse
)

'''-----Predictions on test data and full dataset------'''
# test: select, scale, and project test features using train-fitted scaler/PCA 
test_features = get_selectedfeats_sarcasm( test_names, sarcasm_features_dir, raw_folder_dir, include_lst )
test_features_scaled = scaler.transform(test_features)
test_features_pca = pca.transform( test_features_scaled )

test_pred = predict_classes_test( kmeans, tree, test_features_scaled, test_features_pca, random_state = SEED, split_loworg = split_loworg,
                               idxs_loworg = test_idxs_loworg_sarcasm, reverse=reverse )

# all samples
allsamples_names_lst =  allsamples_names 
allsamples_features = get_selectedfeats_sarcasm( allsamples_names, sarcasm_features_dir, raw_folder_dir, include_lst )
allsamples_features_scaled = scaler.transform(allsamples_features)
allsamples_features_pca = pca.transform( allsamples_features_scaled )

_, allsamples_idxs_loworg_sarcasm = get_loworg_sarcasm( allsamples_names, sarcasm_features_dir)
allsamples_pred = predict_classes_test( kmeans, tree, allsamples_features_scaled, allsamples_features_pca, random_state = SEED, split_loworg = split_loworg,
                               idxs_loworg = allsamples_idxs_loworg_sarcasm, reverse=reverse )
'''----------------------------------------------'''
'''-------------------Results--------------------'''
'''----------------------------------------------'''

'''Figures'''

'''CSV file'''

'''Text files'''






