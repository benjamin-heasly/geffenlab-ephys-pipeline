process geffenlab_ecephys_catgt {
    tag 'geffenlab_ecephys_catgt'
    container 'ghcr.io/benjamin-heasly/geffenlab-spikeglx-tools:v0.0.0'

    publishDir "${params.processed_data_path}/exported",
        mode: 'copy',
        overwrite: true,
        pattern: 'results/*',
        saveAs: { filename -> file(filename).name }

    input:
    path raw_data_path

    output:
    path 'results/*', emit: catgt_results

    script:
    """
    #!/usr/bin/env bash
    set -e

    mkdir -p results/catgt
    conda_run python /opt/code/catgt.py \
      --probe-id $params.probe_id \
      --gate $params.catgt_gate \
      --trigger $params.catgt_trigger \
      $raw_data_path/ecephys \
      results/catgt \
      $params.catgt_args
    """
}

process geffenlab_ecephys_phy_export {
    tag 'geffenlab_ecephys_phy_export'
    container 'ghcr.io/benjamin-heasly/geffenlab-ecephys-phy-export:v0.0.4'

    publishDir "${params.processed_data_path}/exported",
        mode: 'copy',
        overwrite: true,
        pattern: 'results/*',
        saveAs: { filename -> file(filename).name }

    input:
    path processed_data_path

    output:
    path 'results/*', emit: phy_export_results

    script:
    """
    #!/usr/bin/env bash
    set -e

    mkdir -p results
    conda_run python /opt/code/run.py --data-root $processed_data_path --results-root results
    """
}

process geffenlab_ecephys_tprime {
    tag 'geffenlab_ecephys_tprime'
    container 'ghcr.io/benjamin-heasly/geffenlab-spikeglx-tools:v0.0.0'

    publishDir "${params.processed_data_path}/exported",
        mode: 'copy',
        overwrite: true,
        pattern: 'results/*',
        saveAs: { filename -> file(filename).name }

    input:
    path catgt_results
    path phy_export_results

    output:
    path 'results/*', emit: tprime_results

    script:
    """
    #!/usr/bin/env bash
    set -e

    mkdir -p results/tprime
    echo $catgt_results
    ls -alth $catgt_results
    conda_run python /opt/code/tprime.py \
      $catgt_results \
      results/tprime \
      --sync-period $params.tprime_sync_period \
      --to-stream $params.tprime_to_stream \
      --from-streams $params.tprime_from_streams \
      --phy-from-stream $params.tprime_phy_from_stream \
      --probe-id $params.probe_id \
      --phy-pattern $phy_export_results/**/params.py
    """
}

process geffenlab_phy_desktop {
    tag 'geffenlab_phy_desktop'
    container 'ghcr.io/benjamin-heasly/geffenlab-phy-desktop:v0.0.2'

    publishDir "${params.processed_data_path}/curated",
        mode: 'copy',
        overwrite: true,
        pattern: 'results/*',
        saveAs: { filename -> file(filename).name }

    input:
    path phy_export_results

    output:
    path 'results/*', emit: phy_desktop_results

    script:
    """
    #!/usr/bin/env bash
    set -e
    mkdir -p results
    conda_run python /opt/code/run_phy.py \
      --data-root $phy_export_results \
      --results-root results $params.interactive \
      --params-py-pattern **/params.py
    """
}

process geffenlab_synthesis {
    tag 'geffenlab_synthesis'
    container 'ghcr.io/benjamin-heasly/geffenlab-synthesis:v0.0.17'

    publishDir "${params.analysis_path}/synthesis",
        mode: 'copy',
        overwrite: true,
        pattern: 'results/*',
        saveAs: { filename -> file(filename).name }

    input:
    path raw_data_path, name: 'raw_data/'
    path processed_data_path, name: 'processed_data/'
    path phy_export_results, name: 'processed/exported/*'
    path tprime_results, name: 'processed/exported/*'
    path phy_desktop_results, name: 'processed/curated/*'

    output:
    path 'results/*', emit: synthesis_results

    script:
    """
    #!/usr/bin/env bash
    set -e
    mkdir -p results
    conda_run python /opt/code/run.py \
      --raw-data-path=raw_data/ \
      --processed-data-path=processed_data/ \
      --results-path=results \
      --event-times-pattern $params.synthesis_event_times_pattern \
      --experimenter=$params.experimenter \
      --subject=$params.subject \
      --date=$params.date \
      --plotting_scripts $params.synthesis_plotting_scripts
    """
}

workflow {
    println "params: ${params}"

    def raw_data_channel = channel.fromPath(params.raw_data_path)
    catgt_results = geffenlab_ecephys_catgt(raw_data_channel)

    def processed_data_channel = channel.fromPath(params.processed_data_path)
    phy_export_results = geffenlab_ecephys_phy_export(processed_data_channel)
    tprime_results = geffenlab_ecephys_tprime(catgt_results, phy_export_results)
    phy_desktop_results = geffenlab_phy_desktop(phy_export_results)
    geffenlab_synthesis(raw_data_channel, processed_data_channel, phy_export_results, tprime_results, phy_desktop_results)
}
