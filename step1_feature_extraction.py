#---------------Importing modules-------------------
from sarcasm import Structure            
import os
import pandas as pd
from sarcasm.export import Export 
#---------------------Functions-----------------------
def get_filenames_fromfolder(repo_dir, file_format='.tif'):
    # List files in folder and keep only those with the given extension
    sample_names = []
    all_names = os.listdir(repo_dir)
    for name in all_names:
        if name.endswith(file_format):
            # Remove extension so only the base ID is returned
            sample_names.append(name[:-len(file_format)])
    return sample_names
#-----------------Setting up directories---------------
raw_folder_parent_dir = '/projectnb/lejlab2/Sara/Second Project/kazuyas-data-project'
features_folder_parent_dir = ''
abnormalsamples_folder_parent_dir = '/projectnb/lejlab2/Sara/Second Project/kazuyas-data-project'
input_folder_name = 'dataset'
input_folder_dir = os.path.join( raw_folder_parent_dir, input_folder_name)

sample_names = get_filenames_fromfolder( input_folder_dir, file_format = '.tif' ) # List of all .tif samples to be processed
output_folder_name = f'{input_folder_name}_sarcasm_features'
output_folder_dir = os.path.join( features_folder_parent_dir, output_folder_name)
os.makedirs( output_folder_dir, exist_ok=True )
abnormal_samples_dir = os.path.join( abnormalsamples_folder_parent_dir, f'{input_folder_name}_abnormal_samples')
os.makedirs( abnormal_samples_dir, exist_ok = True)

#--------------Extracting and saving features-----------------
pixelsize_um = 0.15   # <-- replace with your microscope’s pixel size in micrometers
# SarcAsM gives us a dictionary of features at the end, but we don’t need all of the features.
# These are the features we exclude when saving the results.
excluded_features_lst = ['axes', 'pixelsize', 'frametime', 'shape_orig', 'shape', 'n_stack', 'size',
           'timestamps', 'file_name', 'file_path', 'time', 'sarcasm_version','timestamp_analysis', 'channel']

# Loop through all samples and extract features
for i, sample_name in enumerate( sample_names ):
    try:
        sarc = Structure(
        os.path.join(input_folder_dir, f"{sample_name}.tif"),
        pixelsize=pixelsize_um
        )
        #------Detecting sarcomeres and extracting features---------------
        sarc.detect_sarcomeres()
        sarc.analyze_cell_mask()
        sarc.analyze_sarcomere_vectors()
        sarc.analyze_z_bands()
        sarc.analyze_myofibrils()
        sarc.analyze_sarcomere_domains()

        sarcdict = Export.get_structure_dict(sarc)

        all_features_lst = sarcdict.keys()
        included_features_lst = list( set(all_features_lst) - set(excluded_features_lst) ) # Keeping only the features we want to save

        features_dict = {}
        for included_features in included_features_lst:
            features_dict[ included_features ] = sarcdict[ included_features ] # Building a clean dictionary of only included features

        #-----------------Saving features as a csv file--------------------
        output_file_dir = os.path.join(  output_folder_dir, f'{sample_name}_features.csv' )
        df = pd.DataFrame(features_dict)
        df.to_csv(output_file_dir, index=False) # Saving one CSV file per sample

        print( f'Extracted features for, {sample_name}, sample {i + 1}')

    except Exception as e: # In case any error happens, the name of the sample and cause of failure is stored in this directory
        err_path = os.path.join(abnormal_samples_dir, f"{sample_name}_errsarcasm.txt")
        with open(err_path, "w") as file:
            file.write(f"sample {sample_name} - {type(e).__name__}: {e}\n")
        print( f"\033[31mSAMPLE {sample_name} - {type(e).__name__}: {e}\033[0m\n" )


