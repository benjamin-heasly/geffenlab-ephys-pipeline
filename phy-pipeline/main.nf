// Eject data from SpikeInterface format to Phy format.
// This produces a phy/ folder similar to what we get from Kilosort.
// But, this version also has quality metrics and automated curation done by SpikeInterface.
process geffenlab_ecephys_phy_export {
    tag 'geffenlab_ecephys_phy_export'
    container 'ghcr.io/benjamin-heasly/geffenlab-ecephys-phy-export:v0.0.7'

    publishDir "${params.analysis_path}/phy-pipeline",
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
    conda_run python /opt/code/run.py \
      --data-root $processed_data_path \
      --results-root results \
      --postprocessed-pattern $params.postprocessed_pattern \
      --curated-pattern $params.curated_pattern
    """
}

// For SpikeGlx recordings, extract events (sync, behavior, stimulus, etc).
process geffenlab_ecephys_catgt {
    tag 'geffenlab_ecephys_catgt'
    container 'ghcr.io/benjamin-heasly/geffenlab-spikeglx-tools:v0.0.4'

    publishDir "${params.analysis_path}/phy-pipeline",
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
      $raw_data_path/ecephys \
      results/catgt \
      --run $params.catgt_run \
      --gate $params.catgt_gate \
      --trigger $params.catgt_trigger \
      --probe-id $params.probe_id \
      $params.catgt_args
    """
}

// For SpikeGlx recordings, align spike times and other events, based on sync events.
process geffenlab_ecephys_tprime {
    tag 'geffenlab_ecephys_tprime'
    container 'ghcr.io/benjamin-heasly/geffenlab-spikeglx-tools:v0.0.4'

    publishDir "${params.analysis_path}/phy-pipeline",
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
      $phy_export_results \
      results/tprime \
      --sync-period $params.tprime_sync_period \
      --to-stream $params.tprime_to_stream \
      --from-streams $params.tprime_from_streams \
      --phy-from-stream $params.tprime_phy_from_stream \
      --probe-id $params.probe_id
    """
}

// TODO: we could add a "bombcell" step here.

// Launch a Phy GUI for manual curation of the sorting results.
// We access this on cortex via remote desktop.
process geffenlab_phy_desktop {
    tag 'geffenlab_phy_desktop'
    container 'ghcr.io/benjamin-heasly/geffenlab-phy-desktop:v0.0.3'

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
      --params-py-pattern **/params.py
    """
}

workflow {
    println "Running phy-pipeline with params: ${params}"

    // Export SpikeInterface results to a phy/ folder in the analysis subdirectory.
    processed_data_channel = channel.fromPath(params.processed_data_path)
    phy_export_results = geffenlab_ecephys_phy_export(processed_data_channel)

    if (params.input == 'spikeglx') {
        // For SpikeGlx, extract events and align spike times offline.
        raw_data_channel = channel.fromPath(params.raw_data_path)
        catgt_results = geffenlab_ecephys_catgt(raw_data_channel)
        tprime_results = geffenlab_ecephys_tprime(catgt_results, phy_export_results)
        if (params.interactive) {
            // Bring up the Phy GUI for manual curation, after making TPrime adjustments.
            geffenlab_phy_desktop(tprime_results)
        }
    } else {
        if (params.interactive) {
            // Bring up the Phy GUI for manual curation, right away.
            geffenlab_phy_desktop(phy_export_results)
        }
    }
}
