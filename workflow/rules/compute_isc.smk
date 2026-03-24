def task_parcel_inputs(wc):
    items = TASK_GROUPS[wc.task]
    return [
        f"../results/parcels/sub-{c['subject']}_task-{c['task']}{c['run_tag']}_space-{c['space']}_res-{c['resolution']}_desc-{c['descriptor']}_parcel_ts.npy"
        for c in items
    ]

rule compute_isc:
    input:
        task_parcel_inputs
    output:
        isc_npy=f"../results/isc/task-{{task}}_isc_mean.npy",
        isc_nii=f"../results/isc/task-{{task}}_isc_mean.nii.gz"
    params:
        n_rois=config["atlas"]["n_rois"],
        yeo_networks=config["atlas"]["yeo_networks"]
    conda:
        "../envs/compute_isc_environment.yaml"
    script:
        "../scripts/compute_isc.py"