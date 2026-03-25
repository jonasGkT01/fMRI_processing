import numpy as np
from nilearn import datasets
from nilearn.maskers import NiftiLabelsMasker

# Snakemake inputs
bold_file = snakemake.input["bold"]
npy_file = snakemake.output["npy"]

n_rois = snakemake.params["n_rois"]
yeo_networks = snakemake.params["yeo_networks"]

print(f"Computing parcels from: {bold_file}")

# Load atlas
atlas = datasets.fetch_atlas_schaefer_2018(
    n_rois=n_rois,
#    data_dir="data/atlases", ##### to modify #####
    yeo_networks=yeo_networks
)

# Create masker
masker = NiftiLabelsMasker(
    labels_img=atlas.maps,
    standardize="zscore_sample",
    detrend=True
)

# Extract time series
ts = masker.fit_transform(bold_file)  # shape: (T, parcels)

# usare libreria logger
# print(f"Output shape: {ts.shape}")

# Save
np.save(npy_file, ts)