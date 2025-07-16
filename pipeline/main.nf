println "params: ${params}"

process geffenlab_ecephys_phy_export {
	tag 'geffenlab_ecephys_phy_export'
	container "ghcr.io/benjamin-heasly/geffenlab-ecephys-phy-export:${params.container_tag}"

    input:
    path data_path
    
    output:
    path 'results/*', emit: results

    publishDir "${params.results_path}", mode: 'copy', overwrite: true, pattern: "results/*"

	script:
	"""
	#!/usr/bin/env bash
	set -e

    mkdir -p results
    /opt/miniconda/bin/conda run --no-capture-output -n ephys-phy-export python -u /opt/code/run.py --data-root $data_path --results-root results
	"""
}

workflow {
    def data = channel.fromPath(params.data_path)
	geffenlab_ecephys_phy_export(data)
}
