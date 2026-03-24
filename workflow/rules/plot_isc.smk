rule plot_isc:
    input:
        ISC_NII_OUTPUTS
    output:
        FIG_PNG_OUTPUTS,
        FIG_HTML_OUTPUTS
    script:
        "../scripts/plot_isc.py"