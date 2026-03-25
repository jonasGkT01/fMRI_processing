import numpy as np
from scipy.stats import pearsonr
from nilearn import datasets, image
import nibabel as nib

# Inputs / outputs
ts_files = list(snakemake.input)
isc_npy = snakemake.output["isc_npy"]
isc_nii = snakemake.output["isc_nii"]

n_rois = snakemake.params["n_rois"]
yeo_networks = snakemake.params["yeo_networks"]

print(f"Computing ISC from {len(ts_files)} BOLD files with {n_rois} parcels each")

# Load atlas
atlas = datasets.fetch_atlas_schaefer_2018(
    n_rois=n_rois,
    yeo_networks=yeo_networks
)
atlas_img = image.load_img(atlas.maps)
atlas_data = atlas_img.get_fdata().astype(int)

# Load parcel data
data = [np.load(f) for f in ts_files]

# Check that all files have the same number of timepoints
time_lengths = [x.shape[0] for x in data]
if len(set(time_lengths)) != 1:
    details = ", ".join(
        f"{f}: {arr.shape[0]} timepoints"
        for f, arr in zip(ts_files, data)
    )
    raise ValueError(f"Mismatched time lengths across input files: {details}")

n_subjects, T, n_parcels = data.shape
print(f"Data shape: {n_subjects} subjects, {T} timepoints, {n_parcels} parcels")

# Compute leave-one-out ISC
isc = np.zeros((n_subjects, n_parcels), dtype=np.float32)

for s in range(n_subjects):
    others_mean = data[np.arange(n_subjects) != s].mean(axis=0)

    for p in range(n_parcels):
        r, _ = pearsonr(data[s, :, p], others_mean[:, p])
        isc[s, p] = np.nan_to_num(r, nan=0.0)

# Average ISC across subjects
isc_mean = isc.mean(axis=0)

# Save parcel ISC
np.save(isc_npy, isc_mean)

# Map back to brain
out_data = np.zeros_like(atlas_data, dtype=np.float32)

for parcel_idx in range(n_parcels):
    label_value = parcel_idx + 1
    out_data[atlas_data == label_value] = isc_mean[parcel_idx]

# Save NIfTI
out_img = nib.Nifti1Image(out_data, affine=atlas_img.affine, header=atlas_img.header)
nib.save(out_img, isc_nii)

print(f"Saved ISC to {isc_npy} and {isc_nii}")