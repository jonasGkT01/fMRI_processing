rule plot_isc:
    input:
        isc_nii=f"../results/isc/task-{{task}}_isc_mean.nii.gz"
    output:
        png=f"../results/figures/task-{{task}}_isc_mean.png",
        html=f"../results/figures/task-{{task}}_isc_mean.html"
    conda:
        "../envs/plot_isc_environment.yaml"
    script:
        "../scripts/plot_isc.py"