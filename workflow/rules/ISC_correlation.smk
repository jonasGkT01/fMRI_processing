rule ISC_correlation:
    input:
        directory(config["ISC_correlation_input"])
    output:
        directory(config["ISC_correlation_output"])
    conda:
        "../envs/ISC_correlation_environment.yaml"
    shell:
        r"""
            python3 scripts/ISC_correlation.py \
                --input {input:q} \
                --output {output:q}
        """