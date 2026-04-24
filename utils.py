import os
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.preprocessing import Normalizer, StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
import tifffile
from sklearn.decomposition import PCA
from ExKMC.Tree import Tree
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import defaultdict

def get_filenames_fromfolder(repo_dir, file_format='.tif'):
    # List files in folder and keep only those with the given extension
    sample_names = []
    all_names = os.listdir(repo_dir)
    for name in all_names:
        if name.endswith(file_format):
            # Remove extension so only the base ID is returned
            sample_names.append(name[:-len(file_format)])
    return sample_names

def print_classcounts(predictions, features_title=''):
    # Print how many samples fall into each class
    print(f'class counts {features_title}:', Counter(predictions))


def get_selectedfeats_sarcasm_single(sample_id, sarcasm_features_dir, include_lst):
    # Load per-sample feature file
    df_file_dir = os.path.join(sarcasm_features_dir, f'{sample_id}_features.csv')
    df = pd.read_csv(df_file_dir)

    # Extract the selected feature columns
    feats = df[include_lst].to_numpy().ravel()

    # Replace missing values with 0
    feats[np.isnan(feats)] = 0.0
    return feats


def get_selectedfeats_sarcasm(sample_ids, sarcasm_features_dir, include_lst):
    # Collect selected features for all samples
    feats_selected = []
    for sample_id in sample_ids:
        feats_selected.append(
            get_selectedfeats_sarcasm_single(sample_id, sarcasm_features_dir, include_lst)
        )
    return feats_selected


def predict_classes_train(features_scaled, features_pca, random_state=1, split_loworg=False,
                          idxs_loworg=None, reverse=False, custom_order=None,
                          loworg_label=0, features_title=''):

    if split_loworg != True:
        # Run KMeans + ExKMC tree on all samples
        k = 3
        kmeans = KMeans(k, random_state=random_state, n_init=10)
        kmeans.fit(features_scaled)

        tree = Tree(k=k, random_state=random_state, max_leaves=2*k)
        predictions = tree.fit_predict(features_scaled, kmeans).astype(np.int64)


        # Relabel clusters based on PCA ordering:
        # smallest mean PC1 → label 0, next → 1, etc. (or reversed/custom)
        predictions_relabeled = relabel_by_mean(features_pca[:, 0], predictions,
                                                reverse=reverse, custom_order=custom_order)

        return predictions_relabeled, kmeans, tree

    else:
        if idxs_loworg is None:
            raise ValueError('Please provide value for idxs_loworg')

        # Separate low-organization samples (given a fixed label)
        mask = np.ones(features_scaled.shape[0], dtype=bool)
        mask[idxs_loworg] = False

        predictions_relabeled = np.zeros(features_scaled.shape[0])
        predictions_relabeled[idxs_loworg] = loworg_label

        # Run clustering only on remaining samples
        features_scaled_sliced = features_scaled[mask]
        features_pca_sliced = features_pca[mask]

        k = 3
        kmeans = KMeans(k, random_state=random_state, n_init=10)
        kmeans.fit(features_scaled_sliced)

        tree = Tree(k=k, random_state=random_state, max_leaves=2*k)
        predictions_sliced = tree.fit_predict(features_scaled_sliced, kmeans).astype(np.int64)

        # Relabel sliced predictions based on PCA mean (same logic as above)
        predictions_relabeled_sliced = relabel_by_mean(features_pca_sliced[:, 0],
                                                       predictions_sliced,
                                                       reverse=reverse,
                                                       custom_order=custom_order)

        # Insert relabeled sliced predictions back into full array
        predictions_relabeled[mask] = predictions_relabeled_sliced

        return predictions_relabeled, kmeans, tree
def predict_classes_test( tree, features_scaled, features_pca, random_state=1,
                         split_loworg=False, idxs_loworg=None, reverse=False,
                         custom_order=None, loworg_label=0, features_title=''):

    if split_loworg != True:
        # Predict cluster IDs using trained tree
        predictions = tree.predict(features_scaled).astype(np.int64)

        # Relabel based on PCA order (lowest mean PC1 → 0, unless reversed/custom)
        predictions_relabeled = relabel_by_mean(features_pca[:, 0], predictions,
                                                reverse=reverse, custom_order=custom_order)

        return predictions_relabeled

    else:
        if idxs_loworg is None:
            raise ValueError('Please provide value for idxs_loworg')

        # Identify low-organization (n_mbands<thresh) samples(kept separate, assigned a fixed label)
        mask = np.ones(features_scaled.shape[0], dtype=bool)
        mask[idxs_loworg] = False

        predictions_relabeled = np.zeros(features_scaled.shape[0])
        predictions_relabeled[idxs_loworg] = loworg_label

        # Predict on the rest of the samples
        features_scaled_sliced = features_scaled[mask]
        features_pca_sliced = features_pca[mask]

        predictions_sliced = tree.predict(features_scaled_sliced).astype(np.int64)

        # Relabel sliced predictions based on PCA mean
        predictions_relabeled_sliced = relabel_by_mean(features_pca_sliced[:, 0],
                                                       predictions_sliced,
                                                       reverse=reverse,
                                                       custom_order=custom_order)

        # Insert relabeled predictions back into full array
        predictions_relabeled[mask] = predictions_relabeled_sliced

        return predictions_relabeled

def get_loworg_sarcasm(sample_ids, sarcasm_features_dir, thresh=0):
    names, indices = [], []

    for idx, sample_id in enumerate(sample_ids):
        # Load per-sample feature file (contains n_mbands = # of sarcomeres)
        df_file_dir = os.path.join(sarcasm_features_dir, f'{sample_id}_features.csv')
        df = pd.read_csv(df_file_dir)

        # Identify very low-organization cells (n_mbands <= thresh).
        # These are set aside (not used in kmeans/tree). The remaining samples
        # will be clustered into 3 groups, and this set-aside group
        # will be added back afterward with a fixed label (default=0),
        # which matches the default label assigned to the lowest-mean PC1 group.
        '''
        Note: In case you are using a different set of features from the
        ones used in this project, you might need to use a custom order
        or a reverse order in "relabel_by_mean". You just need to be careful
        that the fixed low-organization label (default=0) still corresponds
        to the correct end of the ordering — i.e., it should match whichever
        class you treat as the lowest-organization group in your feature space.
        ''' 
        if df['n_mbands'].item() <= thresh:
            names.append(sample_id)
            indices.append(idx)

    # Return the low-org sample IDs and their indices in the full dataset
    return names, np.array(indices)

def relabel_by_mean(X, y, reverse=False, custom_order=None):
    y = np.asarray(y)
    unique_labels = np.unique(y)

    # Compute mean of X (e.g., PC1) for each cluster
    means = {lab: np.mean(X[y == lab]) for lab in unique_labels}

    # Sort clusters by their mean value
    # default: smallest mean → 0, … largest → K-1 (reverse flips this)
    sorted_labels = sorted(unique_labels, key=lambda lab: means[lab], reverse=reverse)

    # Build new label mapping
    if custom_order is None:
        # Default: assign 0..K-1 based on sorted order
        mapping = {old: new for new, old in enumerate(sorted_labels)}
    else:
        # Optional: user-provided label order
        if len(custom_order) != len(sorted_labels):
            raise ValueError("custom_order must match number of classes")
        mapping = {old: new for old, new in zip(sorted_labels, custom_order)}

    # Apply mapping to y
    y_new = np.vectorize(mapping.get)(y).astype(int)
    return y_new

#-----------------------------------------------------
#--------Visualization and evaluation functions-------
#-----------------------------------------------------

def plot_clusters(pca_fit, predictions, title='', saving_dir=None, dpi = 400, label_map = {0: 'l', 1: 'm', 2: 'h'}):
    # Define colors for each predicted class
    colors_dict = {
        "yellow": "#FEEE78",
        "gray":   "#AAAAAA",
        "navy":   "#1D3A62",
    }

    # Map cluster labels → colors
    color_map = {
        0: colors_dict["yellow"],
        1: colors_dict["gray"],
        2: colors_dict["navy"],
    }

    # Scatter-plot PCA points by predicted class
    plt.figure(figsize=(8, 6))
    for lbl in [0, 1, 2]:
        mask = (predictions == lbl)
        plt.scatter(
            pca_fit[mask, 0],
            pca_fit[mask, 1],
            marker='.', s=10,
            color=color_map[lbl],
            label=label_map[lbl]
        )

    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend(markerscale=2, fontsize="small")
    plt.title(title)
    plt.tight_layout()

    # Save figure if path provided
    if saving_dir:
        plt.savefig(saving_dir, dpi=dpi)

    plt.show()

def evaluate_from_confusion(cm, title, class_labels=(0, 1, 2)):
    # Accept confusion matrix as DataFrame or ndarray
    if isinstance(cm, pd.DataFrame):
        cm_values = cm.values
        labels = list(class_labels)
        cm_df = cm.copy()
    else:
        cm_values = np.asarray(cm)
        labels = list(class_labels)
        cm_df = pd.DataFrame(
            cm_values,
            index=pd.Index(labels, name="true"),
            columns=pd.Index(labels, name="pred")
        )

    # Ensure matrix size matches expected labels
    k = len(labels)
    if cm_values.shape != (k, k):
        raise ValueError(f"Confusion matrix must be {k}x{k} for labels {labels}.")

    # Basic counts per class
    tp = np.diag(cm_values).astype(float)
    support = cm_values.sum(axis=1).astype(float)      # true counts
    pred_counts = cm_values.sum(axis=0).astype(float)  # predicted counts
    total = cm_values.sum().astype(float)

    # Standard precision/recall/accuracy
    accuracy = (tp.sum() / total) if total > 0 else np.nan
    precision = np.divide(tp, pred_counts, out=np.zeros_like(tp), where=pred_counts > 0)
    recall = np.divide(tp, support, out=np.zeros_like(tp), where=support > 0)

    macro_precision = float(np.nanmean(precision)) if k > 0 else np.nan
    macro_recall = float(np.nanmean(recall)) if k > 0 else np.nan

    # Table of per-class metrics
    per_class = pd.DataFrame({
        "precision": precision,
        "recall": recall,
        "gnd_counts": support,
        "predicted_counts": pred_counts,
        "tp": tp
    }, index=labels)

    # Overall summary metrics
    overall = pd.DataFrame({
        "accuracy": [float(accuracy)],
        "macro_precision": [macro_precision],
        "macro_recall": [macro_recall],
    })

    # Printing
    def fmt(a, n=3):
        return np.array2string(np.asarray(a), precision=n, floatmode='fixed')

    print(f"\nFor {title} metrics are:")
    print(f"  Accuracy: {accuracy:.3f}")
    print(f"  Macro precision: {macro_precision:.3f}  |  Macro recall: {macro_recall:.3f}")
    print(f"  Per-class precision: {fmt(precision)}")
    print(f"  Per-class recall:    {fmt(recall)}")

    return cm_df, overall, per_class

def plot_pca_matches(features_pca, labels_gnd, labels_pred, title="Ground truth vs predicted labels", saving_dir = None, dpi = 400):
    """
    Scatter PCA[:,0] vs PCA[:,1]. Green = y_true==y_pred, Red = mismatch.
    Works whether inputs are lists, numpy arrays, or pandas objects.
    """
    # Cast everything to NumPy
    X = np.asarray(features_pca)
    y_true = np.asarray(labels_gnd).ravel()
    y_pred = np.asarray(labels_pred).ravel()

    # Basic checks
    if X.ndim != 2 or X.shape[1] < 2:
        raise ValueError("features_pca must have shape (n_samples, >= 2).")
    if len(y_true) != len(y_pred) or len(y_true) != X.shape[0]:
        raise ValueError("features and labels must have the same number of samples.")

    matches = (y_true == y_pred)

    # Set up axes
    fig, ax = plt.subplots(figsize=(6, 6))


    # Plot
    ax.scatter(X[matches, 0], X[matches, 1],
               c="green", label=f"Match ({matches.sum()})",
               alpha=0.7, edgecolors="k")
    ax.scatter(X[~matches, 0], X[~matches, 1],
               c="red", label=f"Mismatch ({(~matches).sum()})",
               alpha=0.7, edgecolors="k")

    # Labels/legend
    ax.set_xlabel("PCA Component 1")
    ax.set_ylabel("PCA Component 2")
    ax.set_title(title)
    ax.legend()


    plt.tight_layout()
    # Save figure if path provided
    if saving_dir:
        plt.savefig(saving_dir, dpi=dpi)

    plt.show()

def samples_by_label_pair(y_true, y_pred, X, labels=None, include_empty=False):
    # Convert inputs to arrays
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    X = np.asarray(X)

    if not (len(y_true) == len(y_pred) == len(X)):
        raise ValueError("y_true, y_pred, and X must have the same length.")

    # Group sample IDs by (true_label, pred_label)
    buckets = defaultdict(list)
    for sample_id, t, p in zip(X, y_true, y_pred):
        buckets[(t, p)].append(sample_id)

    # Determine list of labels to iterate over
    if labels is None:
        labels = np.array(sorted(set(np.unique(y_true)) | set(np.unique(y_pred))))
    else:
        labels = np.array(labels)

    # Build mapping for all (true, pred) pairs
    out = {}
    for t in labels:
        for p in labels:
            samples = buckets.get((t, p), [])
            # include_empty=False → only return pairs that actually occurred
            # include_empty=True  → explicitly include empty lists for missing pairs
            if include_empty or samples:
                out[(t, p)] = samples
    return out

def pick_random_per_pair(labelpairs_dict, seed=0):
    rng = np.random.default_rng(seed)

    out = {}
    for key, samples in labelpairs_dict.items():
        if samples:
            out[key] = rng.choice(samples)
        else:
            out[key] = None
    return out


def plot_gndvspred(pair_key, sample_id, raw_folder_dir,
                   zdiscs_plot_thresh=0.1,
                   label_map={0: 'low', 1: 'medium', 2: 'high'}, saving_dir = None, dpi = 400):

    # Load raw image and z-discs
    raw_image = tifffile.imread(os.path.join(raw_folder_dir, f'{sample_id}.tif')).astype(np.float32)
    zdiscs = tifffile.imread(os.path.join(raw_folder_dir, f'{sample_id}/zbands.tif'))

    # Set up figure with three panels
    fig, axes = plt.subplots(1, 3, figsize=(14, 7), sharex=True, sharey=True)

    # --- Panel 1: raw image with ground-truth label ---
    axes[0].imshow(raw_image, cmap="gray")
    axes[0].set_title(f"Raw image: \n {sample_id} \n Ground truth label: {label_map[pair_key[0]]}")
    axes[0].axis("off")

    # Create overlay mask for z-discs above threshold
    color = (1.0, 0.0, 0.0)  # red overlay
    alpha = 1
    mask = zdiscs > zdiscs_plot_thresh
    overlay = np.zeros((*mask.shape, 4), dtype=float)  # RGBA overlay
    overlay[mask] = (*color, alpha)

    # --- Panel 2: raw image with z-disc overlay + predicted label ---
    axes[1].imshow(raw_image, cmap='gray')
    axes[1].imshow(overlay, interpolation='nearest')
    axes[1].set_title(f"Zdiscs (overlay) \n Predicted label: {label_map[pair_key[1]]}")
    axes[1].axis("off")

    # --- Panel 3: z-disc mask alone ---
    axes[2].imshow(zdiscs, cmap='gray')
    axes[2].set_title("Zdiscs")
    axes[2].axis("off")

    if saving_dir:
        plt.savefig(saving_dir, dpi = dpi)
