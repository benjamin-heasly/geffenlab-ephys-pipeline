// Export data from SpikeInterface format, save in Phy format.
// This produces an exported/phy/ folder similar to what we get from Kilosort.
// But, this version also has quality metrics and automated curation done by SpikeInterface.
process geffenlab_ecephys_phy_export {
    tag 'geffenlab_ecephys_phy_export'
    container 'ghcr.io/benjamin-heasly/geffenlab-ecephys-phy-export:v0.0.11'

    publishDir "${params.analysis_path}/phy-export/$params.ecephys_session_name",
        mode: 'copy',
        overwrite: true,
        pattern: 'results/*',
        saveAs: { filename -> file(filename).name }

    input:
    path ecephys_path
    path processed_data_path

    output:
    path 'results/*', emit: phy_export_results

    script:
    """
    #!/usr/bin/env bash
    set -e

    mkdir -p results/exported
    conda_run python /opt/code/run.py \
      --ecephys-dir $ecephys_path \
      --processed-data-dir $processed_data_path \
      --results-dir \$PWD/results/exported \
      --preprocessed-pattern $params.preprocessed_pattern \
      --postprocessed-pattern $params.postprocessed_pattern \
      --curated-pattern $params.curated_pattern \
      --compute-pc-features true \
      --copy-binary false \
      --export-sparse false \
      --n-jobs $params.n_jobs
    """
}

// For SpikeGlx recordings, extract events (sync, behavior, stimulus, etc).
process geffenlab_ecephys_catgt {
    tag 'geffenlab_ecephys_catgt'
    container 'ghcr.io/benjamin-heasly/geffenlab-spikeglx-tools:v0.0.10'

    publishDir "${params.analysis_path}/phy-export/$params.ecephys_session_name",
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
      $raw_data_path/ecephys/$params.ecephys_session_name \
      results/catgt \
      $params.catgt_args
    """
}

// For SpikeGlx recordings, align spike times and other events, based on sync events.
process geffenlab_ecephys_tprime {
    tag 'geffenlab_ecephys_tprime'
    container 'ghcr.io/benjamin-heasly/geffenlab-spikeglx-tools:v0.0.10'

    publishDir "${params.analysis_path}/phy-export/$params.ecephys_session_name",
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
      --phy-from-pattern $params.tprime_phy_from_pattern
    """
}

// Do "bombcell" curation and visualization on the SpikeGlx/TPrime or Open Ephys phy/ output.
process geffenlab_ecephys_bombcell {
    tag 'geffenlab_ecephys_bombcell'
    container 'ghcr.io/benjamin-heasly/geffenlab-bombcell:v0.0.2'

    input:
    path phy_dir
    val bombcell_params_json

    output:
    path 'results/*'
    path "$phy_dir/phy/*"

    // Publish Bombcell results like diagnostic plots.
    publishDir "${params.analysis_path}/phy-export/$params.ecephys_session_name/bombcell/other",
        mode: 'copy',
        overwrite: true,
        pattern: 'results/*',
        saveAs: { filename -> file(filename).name }

    // Publish a version of the Phy dir(s) that include TSVs from Bombcell.
    publishDir "${params.analysis_path}/phy-export/$params.ecephys_session_name/bombcell/phy",
        mode: 'copy',
        overwrite: true,
        pattern: "$phy_dir/phy/*",
        saveAs: { filename -> file(filename).name }

    script:
    """
    #!/usr/bin/env bash
    set -e

    mkdir -p results
    conda_run python /opt/code/run.py \
      --phy-root $phy_dir \
      --phy-pattern "phy/*/params.py" \
      --bombcell-params-json '$bombcell_params_json' \
      --results-dir \$PWD/results \
    """
}

workflow {
    println "Running phy-export with params: ${params}"

    // Load Bombcell params from JSON, to pass to the bombcell step.
    String bombcell_params_json = '{}'
    if (params.bombcell_params_file) {
        bombcell_params_json = file(params.bombcell_params_file).text
    }

    // Export SpikeInterface results to a phy/ folder in the analysis subdirectory.
    processed_data_channel = channel.fromPath(params.processed_data_path)
    ecephys_channel = channel.fromPath(params.ecephys_path)
    phy_export_results = geffenlab_ecephys_phy_export(ecephys_channel, processed_data_channel)

    if (params.input == 'spikeglx') {
        // For SpikeGlx, extract events and align spike times offline.
        raw_data_channel = channel.fromPath(params.raw_data_path)
        catgt_results = geffenlab_ecephys_catgt(raw_data_channel)
        tprime_results = geffenlab_ecephys_tprime(catgt_results, phy_export_results)

        // Run bombcell on the TPrime-adjusted phy/ dir.
        geffenlab_ecephys_bombcell(tprime_results, bombcell_params_json)
    } else {
        // Run bombcell on phy/ dir exported from Spike Interface.
        geffenlab_ecephys_bombcell(phy_export_results, bombcell_params_json)
    }
}
