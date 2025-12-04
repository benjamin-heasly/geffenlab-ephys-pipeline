// Export data from SpikeInterface format, save in Phy format.
// This produces an exported/phy/ folder similar to what we get from Kilosort.
// But, this version also has quality metrics and automated curation done by SpikeInterface.
process geffenlab_ecephys_phy_export {
    tag 'geffenlab_ecephys_phy_export'
    container 'ghcr.io/benjamin-heasly/geffenlab-ecephys-phy-export:v0.0.9'

    publishDir "${params.analysis_path}/phy-export",
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

    mkdir -p results/exported/$params.ecephys_session_name
    conda_run python /opt/code/run.py \
      --data-root $processed_data_path \
      --results-root results/exported/$params.ecephys_session_name \
      --postprocessed-pattern $params.postprocessed_pattern \
      --curated-pattern $params.curated_pattern
    """
}

// For SpikeGlx recordings, extract events (sync, behavior, stimulus, etc).
process geffenlab_ecephys_catgt {
    tag 'geffenlab_ecephys_catgt'
    container 'ghcr.io/benjamin-heasly/geffenlab-spikeglx-tools:v0.0.10'

    publishDir "${params.analysis_path}/phy-export",
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

    mkdir -p results/catgt/$params.ecephys_session_name
    conda_run python /opt/code/catgt.py \
      $raw_data_path/ecephys/$params.ecephys_session_name \
      results/catgt/$params.ecephys_session_name \
      $params.catgt_args
    """
}

// For SpikeGlx recordings, align spike times and other events, based on sync events.
process geffenlab_ecephys_tprime {
    tag 'geffenlab_ecephys_tprime'
    container 'ghcr.io/benjamin-heasly/geffenlab-spikeglx-tools:v0.0.10'

    publishDir "${params.analysis_path}/phy-export",
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

    mkdir -p results/tprime/$params.ecephys_session_name
    echo $catgt_results
    ls -alth $catgt_results
    conda_run python /opt/code/tprime.py \
      $catgt_results/$params.ecephys_session_name \
      $phy_export_results/$params.ecephys_session_name \
      results/tprime/$params.ecephys_session_name \
      --sync-period $params.tprime_sync_period \
      --to-stream $params.tprime_to_stream \
      --from-streams $params.tprime_from_streams \
      --phy-from-pattern $params.tprime_phy_from_pattern
    """
}

// Do "bombcell" curation and visualization on the SpikeGlx/TPrime or Open Ephys phy/ output.
// TODO: this is a placeholder for now!
process geffenlab_ecephys_bombcell {
    tag 'geffenlab_ecephys_bombcell'
    container 'ubuntu'

    publishDir "${params.analysis_path}/phy-export",
        mode: 'copy',
        overwrite: true,
        pattern: 'results/*',
        saveAs: { filename -> file(filename).name }

    input:
    path phy_dir

    output:
    path 'results/*', emit: bombcell_results

    script:
    """
    #!/usr/bin/env bash
    set -e

    mkdir -p results/bombcell/$params.ecephys_session_name
    echo "$phy_dir" > results/bombcell/$params.ecephys_session_name/TODO.txt
    """
}

workflow {
    println "Running phy-export with params: ${params}"

    // Export SpikeInterface results to a phy/ folder in the analysis subdirectory.
    processed_data_channel = channel.fromPath(params.processed_data_path)
    phy_export_results = geffenlab_ecephys_phy_export(processed_data_channel)

    if (params.input == 'spikeglx') {
        // For SpikeGlx, extract events and align spike times offline.
        raw_data_channel = channel.fromPath(params.raw_data_path)
        catgt_results = geffenlab_ecephys_catgt(raw_data_channel)
        tprime_results = geffenlab_ecephys_tprime(catgt_results, phy_export_results)

        // Run bombcell on the TPrime-adjusted phy/ dir.
        bombcell_results = geffenlab_ecephys_bombcell(tprime_results)
    } else {
        // Run bombcell on phy/ dir exported from Spike Interface.
        bombcell_results = geffenlab_ecephys_bombcell(phy_export_results)
    }
}
