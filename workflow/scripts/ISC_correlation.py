# load brain parcellation atlas
from nilearn import datasets

atlas = datasets.fetch_atlas_schaefer_2018(n_rois=200, yeo_networks=7)

atlas_img = atlas.maps   # NIfTI file
labels = atlas.labels    # parcel names

# load bold files wrt given task
import argparse
import glob

parser = argparse.ArgumentParser()
parser.add_argument("--input",  help="Input directory containing bold files")
parser.add_argument("--output", help="Output directory for results")
parser.add_argument("--task",   help="Task name for which ISC correlation is computed")
args = parser.parse_args()

bold_files = sorted(glob.glob(f"{args.input}/sub-*/func/*_task-{args.task}*_bold.nii.gz"))

print(len(bold_files), "subjects found")

# extract parcel time series for each subject
from nilearn.maskers import NiftiLabelsMasker

masker = NiftiLabelsMasker(
    labels_img=atlas_img,
    standardize=True,      # z-score per voxel → important
    detrend=True,
    low_pass=None,
    high_pass=None,
    t_r=None               # optional, set if known
)

parcel_timeseries = []

for f in bold_files:
    ts = masker.fit_transform(f)   # shape: (T, parcels)
    parcel_timeseries.append(ts)

# check that all subjects have the same number of parcels and time points
shapes = [ts.shape for ts in parcel_timeseries]
print(set(shapes))

# stack parcel time series across subjects
import numpy as np

data = np.stack(parcel_timeseries)  
# shape: (subjects, T, parcels)

# compute group mean
group_mean = data.mean(axis=0)  
# shape: (T, parcels)

# compute ISC for each subject and parcel
from scipy.stats import pearsonr

n_subjects, T, n_parcels = data.shape

isc = np.zeros((n_subjects, n_parcels))

for s in range(n_subjects):
    others_mean = data[np.arange(n_subjects) != s].mean(axis=0)
    
    for p in range(n_parcels):
        r, _ = pearsonr(data[s, :, p], others_mean[:, p])
        isc[s, p] = r

isc_mean = isc.mean(axis=0)  
# shape: (parcels,)

# print top parcels with highest ISC
top_idx = np.argsort(isc_mean)[-10:]

for i in top_idx:
    print(i, labels[i], isc_mean[i])

# visualize ISC map
from nilearn import plotting

plotting.plot_stat_map(
    atlas_img,
    title="ISC Correlation (mean across subjects)",
)