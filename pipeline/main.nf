println "params: ${params}"

process geffenlab_ecephys_catgt {
    tag 'geffenlab_ecephys_catgt'
    container 'ghcr.io/benjamin-heasly/geffenlab-spikeglx-tools:v0.0.0'

    input:
    path data_path

    output:
    path 'results/*', emit: catgt_results

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
    path 'results/*', emit: phy_export_results

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

process geffenlab_ecephys_tprime {
    tag 'geffenlab_ecephys_tprime'
    container 'ghcr.io/benjamin-heasly/geffenlab-spikeglx-tools:v0.0.0'

    input:
    path catgt_results
    path phy_export_results

    output:
    path 'results/*', emit: tprime_results

    publishDir "${params.analysis_path}/exported",
        mode: 'copy',
        overwrite: true,
        pattern: 'results/*',
        saveAs: { filename -> file(filename).name }

    script:
    """
    #!/usr/bin/env bash
    set -e

    mkdir -p results/tprime
    conda_run python /opt/code/tprime.py \
      $catgt_results \
      results/tprime \
      --sync-period 1.0 \
      --to-stream **/**/*imec0.ap.*.txt \
      --from-streams \
        **/*nidq.xd_8_4_500.txt:**/*nidq.xa_0_500.txt \
        **/*nidq.xd_8_4_500.txt:**/*nidq.xia_1_0.txt \
        **/*nidq.xd_8_4_500.txt:**/*nidq.xd_8_3_0.txt \
        **/*nidq.xd_8_4_500.txt:**/*nidq.xid_8_2_1p7.txt \
        **/*nidq.xd_8_4_500.txt:**/*nidq.xid_8_3_5.txt \
      --phy-from-stream **/**/*imec0.ap.*.txt \
      --probe-id block0_imec0.ap_recording1 \
      --phy-pattern $phy_export_results/**/params.py
    """
}

process geffenlab_phy_desktop {
    tag 'geffenlab_phy_desktop'
    container 'ghcr.io/benjamin-heasly/geffenlab-phy-desktop:v0.0.1'

    input:
    path phy_export_results

    output:
    path 'results/*', emit: phy_desktop_results

    publishDir "${params.analysis_path}/curated",
        mode: 'copy',
        overwrite: true,
        pattern: 'results/*',
        saveAs: { filename -> file(filename).name }

    script:
    """
    #!/usr/bin/env bash
    set -e
    mkdir -p results
    conda_run python /opt/code/run_phy.py --data-root $phy_export_results --results-root results $params.interactive --params-py-pattern **/params.py
    """
}

process geffenlab_synthesis {
    tag 'geffenlab_synthesis'
    container 'ghcr.io/benjamin-heasly/geffenlab-synthesis:v0.0.4'

    input:
    path data_path
    path phy_export_results, name: "analysis/exported/*"
    path tprime_results, name: "analysis/exported/*"
    path phy_desktop_results, name: "analysis/curated/*"

    output:
    path 'results/*', emit: synthesis_results

    publishDir "${params.analysis_path}/synthesis",
        mode: 'copy',
        overwrite: true,
        pattern: 'results/*',
        saveAs: { filename -> file(filename).name }

    script:
    """
    #!/usr/bin/env bash
    set -e
    mkdir -p results
    conda_run python /opt/code/run.py --data-path=$data_path --analysis-path=analysis --results-path=results
    """
}

workflow {
    def data_channel = channel.fromPath(params.data_path)
    catgt_results = geffenlab_ecephys_catgt(data_channel)

    def analysis_channel = channel.fromPath(params.analysis_path)
    phy_export_results = geffenlab_ecephys_phy_export(analysis_channel)

    tprime_results = geffenlab_ecephys_tprime(catgt_results, phy_export_results)

    phy_desktop_results = geffenlab_phy_desktop(phy_export_results)

    synthesis_results = geffenlab_synthesis(data_channel, phy_export_results, tprime_results, phy_desktop_results)
}
