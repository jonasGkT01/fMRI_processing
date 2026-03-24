rule compute_isc:
    input:
        PARCEL_OUTPUTS
    output:
        ISC_NPY_OUTPUTS,
        ISC_NII_OUTPUTS
    params:
        n_rois=config["atlas"]["n_rois"],
        yeo_networks=config["atlas"]["yeo_networks"]
    script:
        "../scripts/compute_isc.py"