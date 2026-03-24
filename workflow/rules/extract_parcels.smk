rule extract_parcels:
    input:
        bold=lambda wc: config["bold_glob_pattern"].format(
            subject=wc.subject,
            task=wc.task,
            run_tag=wc.run_tag,
            space=wc.space,
            resolution=wc.resolution,
            descriptor=wc.descriptor,
        )
    output:
        npy=f"../results/parcels/sub-{{subject}}_task-{{task}}{{run_tag}}_space-{{space}}_res-{{resolution}}_desc-{{descriptor}}_parcel_ts.npy"
    params:
        n_rois=config["atlas"]["n_rois"],
        yeo_networks=config["atlas"]["yeo_networks"]
    script:
        "../scripts/extract_parcels.py"