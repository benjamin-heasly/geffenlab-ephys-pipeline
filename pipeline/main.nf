println "params: ${params}"

process geffenlab_ecephys_catgt {
    tag 'geffenlab_ecephys_catgt'
    container 'geffenlab/geffenlab-spikeglx-tools:local'
    //container "ghcr.io/benjamin-heasly/geffenlab/geffenlab-spikeglx-tools:${params.container_tag}"

    input:
    path data_path

    output:
    path 'results/*', emit: results

    publishDir "${params.analysis_path}/exported",
        mode: 'copy',
        overwrite: true,
        pattern: 'results/*',
        saveAs: { filename -> file(filename).name }

    script:
    """
    #!/usr/bin/env bash
    set -e

    mkdir -p results/catgt
    conda_run python /opt/code/catgt.py \
      --probe-id imec0 \
      --gate 0 \
      --trigger 0 \
      $data_path/ecephys \
      results/catgt \
      AS20_03112025_trainingSingle6Tone2024_Snk3.1 \
      -ni -ap -prb_fld -out_prb_fld -no_tshift \
      -xa=0,0,0,1,3,500 -xia=0,0,1,3,3,0 -xd=0,0,8,3,0 -xid=0,0,-1,2,1.7 -xid=0,0,-1,3,5
    """
}

process geffenlab_ecephys_phy_export {
    tag 'geffenlab_ecephys_phy_export'
    container 'ghcr.io/benjamin-heasly/geffenlab-ecephys-phy-export:v0.0.4'

    input:
    path analysis_path

    output:
    path 'results/*', emit: results

    publishDir "${params.analysis_path}/exported",
        mode: 'copy',
        overwrite: true,
        pattern: 'results/*',
        saveAs: { filename -> file(filename).name }

    script:
    """
    #!/usr/bin/env bash
    set -e

    mkdir -p results
    conda_run python /opt/code/run.py --data-root $analysis_path --results-root results
    """
}

workflow {
    // def data_channel = channel.fromPath(params.data_path)
    // catgt_results = geffenlab_ecephys_catgt(data_channel)

    def analysis_channel = channel.fromPath(params.analysis_path)
    phy_results = geffenlab_ecephys_phy_export(analysis_channel)
}
