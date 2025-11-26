# This script creates a new CSV file called 'metadata_split.csv'.
# In this step, train/test labels are assigned to samples.
# The 'test' set corresponds to samples originally located in specific folders:
#     "03_FN_P5D2", "04_VN_P5D2", "05_FN_Cilen100", "06_VN_Cilen100"
# All other samples are labeled as 'train'.

#---------------Importing modules-------------------
import os
import pandas as pd

#---------------File setup--------------------------
parent_dir = ''
csv_files_folder = 'csv_files'
metadata_base_name = 'metadata_base.csv'
metadata_base_dir = os.path.join(parent_dir, csv_files_folder, metadata_base_name)

output_file_dir = os.path.join(parent_dir, csv_files_folder, "metadata_split.csv")
#---------------Read metadata-----------------------
df = pd.read_csv(metadata_base_dir)

# Make a copy
df_new = df.copy()

# You can change this part to assign train/test randomly, 
# but be careful: ground truth (gnd) must be available for the test set, 
# while it is not required for the training set.

#---------------Define test folders-----------------
test_folders = ["03_FN_P5D2", "04_VN_P5D2", "05_FN_Cilen100", "06_VN_Cilen100"]

#---------------Assign train/test split-------------
df_new["split"] = df_new["orig_folder"].apply(
    lambda x: "test" if x in test_folders else "train"
)

#---------------Save the new CSV---------------------
df_new.to_csv(output_file_dir, index=False)

print(f"Saved: {output_file_dir}")
