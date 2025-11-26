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
np.random.seed(SEED)

'''------Setting up directories------------'''
#----Parent directories----
dataset_parent_dir = '/projectnb/lejlab2/Sara/Second Project/kazuyas-data-project'
csvfiles_parent_dir = ''
figures_parent_dir = ''
textresults_parent_dir = ''

#----Folders---
# Raw data folder
raw_folder_name = 'dataset'
raw_folder_dir = os.path.join(dataset_parent_dir, raw_folder_name)

# Folder with per-sample sarcasm feature files
sarcasm_features_folder_name = f'{raw_folder_name}_sarcasm_features'
sarcasm_features_dir = os.path.join(dataset_parent_dir, sarcasm_features_folder_name)

# Count available samples based on feature files
print("Total number of data samples is:",
      len(get_filenames_fromfolder(sarcasm_features_dir, file_format="_features.csv")))

# Folder for CSV files
csvfiles_folder_name = 'csv_files'
csvfiles_folder_dir = os.path.join(csvfiles_parent_dir, csvfiles_folder_name)

# Folder for figures
figures_folder_name = 'figures'
figures_folder_dir = os.path.join(figures_parent_dir, figures_folder_name)
os.makedirs( figures_folder_dir, exist_ok = True)

# Folder for text results
textresults_folder_name = 'text_results'
textresults_folder_dir = os.path.join(textresults_parent_dir, textresults_folder_name)

#----Directories for metadata---

# Path to metadata CSV file
metadata_features_csv_dir  = os.path.join(csvfiles_folder_dir, 'metadata_features.csv')  

#----Directories for analysis results---
# Figures
cluster_train_figure_dir = f'{figures_folder_dir}/clusters_train.png'
cluster_test_figure_dir = f'{figures_folder_dir}/clusters_test.png'
mismatches_test_figure_dir = f'{figures_folder_dir}/mismatch_test.png'
cm_test_figure_dir = f'{figures_folder_dir}/cm_test.png'
def get_gndvspred_figure_dir( figures_folder_dir, pair_key):
      return f'{figures_folder_dir}/gnd{int(pair_key[0])}_pred{int(pair_key[1])}.png'

# CSVs
cm_test_csv_dir = f'{csvfiles_folder_dir}/cm_test.csv'
perclass_test_csv_dir = f'{csvfiles_folder_dir}/perclass_test.csv'
summary_test_csv_dir = f'{csvfiles_folder_dir}/summary_test.csv'

# Txts
PC_train_txt_dir = f'{textresults_folder_dir}/PC_train.txt'
PC_test_txt_dir = f'{textresults_folder_dir}/PC_test.txt'

print('Set up directories')

'''------Train and test------------'''
# Load metadata
df = pd.read_csv(metadata_features_csv_dir)

# Separate train and test samples
df_train = df[df["split"] == "train"].copy()
df_test  = df[df["split"] == "test"].copy()

# Train set: names, predictions and principal components of features
train_names = df_train['name'].to_list()
train_pred = df_train['group_pred'].to_numpy()
train_features_pca = np.loadtxt( PC_train_txt_dir )

# Test set: names + ground-truth labels + low-org indices
test_names  = df_test['name'].to_list()
test_labels = df_test['group_gnd'].to_numpy()
test_pred = df_test['group_pred'].to_numpy()
test_features_pca = np.loadtxt( PC_test_txt_dir )

print('Set up train and test')
'''----------------------------------------------'''
'''-------------------Results--------------------'''
'''----------------------------------------------'''
# Analysis: confusion matrix
cm_test = confusion_matrix(test_labels, test_pred, labels=[0, 1, 2])
cm_test_df, overall_test, per_class_test = evaluate_from_confusion( cm_test, title = 'test')

print('Confusion matrix analysis for the test data was done')
'''Figures'''
# Clusters
plot_clusters( train_features_pca,  train_pred, title = 'Train: group prediction', saving_dir = cluster_train_figure_dir)
plot_clusters( test_features_pca,  test_pred, title = 'Test: group prediction', saving_dir = cluster_test_figure_dir)
print( 'Saved figures: clusters, train and test')

# Mismatches
plot_pca_matches( test_features_pca, np.array( test_labels ), test_pred, title="Test: ground truth vs predicted labels", saving_dir = mismatches_test_figure_dir )
print( 'Saved figure: mismatches, test')

# confustion matrix
class_names = ['l', 'm', 'h']
disp = ConfusionMatrixDisplay(confusion_matrix=cm_test, display_labels=class_names)
plt.figure()
disp.plot()
disp.ax_.set(xlabel='prediction', ylabel='ground truth')
plt.title("Confusion matrix (test data)")
plt.savefig(cm_test_figure_dir, dpi = 400)
print( 'Saved figure: confusion matrix, test')

#------------------
# Grouping test samples by (true_label, pred_label), include empty pairs as well
labelpairs_dict = samples_by_label_pair(test_labels, test_pred, test_names, include_empty=True)

# Picking one random sample ID from each (true, pred) pair
random_samples_dict = pick_random_per_pair(labelpairs_dict, seed = SEED)

# Plotting the chosen sample for each pair (or reporting if none exist)
for pair_key, sample_id in random_samples_dict.items():
    if sample_id:
        plot_gndvspred(pair_key, sample_id, raw_folder_dir, saving_dir = get_gndvspred_figure_dir( figures_folder_dir, pair_key))
        print( f'Saved figure: gndvspred {pair_key}, test')
    else:
        print( f'No samples for {pair_key} key')

'''CSV file'''
# Results as csv files
cm_test_df.to_csv( cm_test_csv_dir)
per_class_test.to_csv( perclass_test_csv_dir)
overall_test.to_csv( summary_test_csv_dir )


'''Text files'''
np.savetxt(PC_train_txt_dir, train_features_pca)
np.savetxt(PC_test_txt_dir, test_features_pca)





