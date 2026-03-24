import numpy as np
from nilearn import datasets
from nilearn.maskers import NiftiLabelsMasker

# Snakemake inputs
bold_file = snakemake.input["bold"]
out_file = snakemake.output["npy"]

n_rois = snakemake.params["n_rois"]
yeo_networks = snakemake.params["yeo_networks"]

print(f"Extracting parcels from: {bold_file}")

# Load atlas
atlas = datasets.fetch_atlas_schaefer_2018(
    n_rois=n_rois,
    yeo_networks=yeo_networks
)

# Create masker
masker = NiftiLabelsMasker(
    labels_img=atlas.maps,
    standardize=True,   # z-score (important)
    detrend=True
)

# Extract time series
ts = masker.fit_transform(bold_file)  # shape: (T, parcels)

print(f"Output shape: {ts.shape}")

# Save
np.save(out_file, ts)