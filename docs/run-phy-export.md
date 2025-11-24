# Run Geffen lab Phy export

This doc should help you run the Geffen lab's [phy-export.nf](../phy-export/phy-export.nf) Nextflow pipeline.
This will export sorting and SpikeInterface curation results from the AIND ephys pipeline, to the format used by Phy.

For SpikeGlx recordings, this also includes running CatGT to extract events and TPrime to align events and spike times.

Before running this you must run the AIND ephys pipeline for your session: [run-aind-ephys-pipeline.md](./run-aind-ephys-pipeline.md)


## Pipeline configuration and arguments

We use our own Nextflow pipline defined in [phy-export.nf](../phy-export/phy-export.nf) to export AIND ephys pipeline results to Phy.

We combine this with a Nextflow configuration file which tells Nextflow to do things like:
 - Locate Geffen lab data and results within `/vol/cortex/cd4/geffenlab/`.
 - Share CPU, GPU, and RAM with other cortex users.

To run the pipeline, use our Python script [run_pipeline.py](./scripts/run_pipeline.py).
This script calls `nextflow run` for the pipeline itself, and also saves detailed logs within the `processed_data` subdirectory directory for each session.

We tell the script which pipeline to run with the `--workflow` argument.  We specifiy the configuration to use with `--config`.  We also pass the `experimenter`, `--subject`, and `--date` for the session we want to process.

The `--input` parameter can be `spikeglx` or `openephys`, to tell whether we need to run CatGT and TPrime.

## Run the pipeline

To run the pipeline, connect to cortex via remote desktop and open a terminal window.
Run the following command (or similar, depending on your data).

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow geffenlab-ephys-pipeline/phy-export/phy-export.nf \
  --config geffenlab-ephys-pipeline/phy-export/cortex.config \
  --experimenter BH \
  --subject AS20-minimal3 \
  --date 03112025 \
  --input spikeglx
```

The pipeline run should take less than an hour.  A clean run should end with a summary like this:

```
Completed at: 14-Aug-2025 15:16:36
Duration    : 5m 17s
CPU hours   : 0.7
Succeeded   : 12
```

## Results overview

The pipeline looks for processed session data within the lab's sotrage directory, `/vol/cortex/cd4/geffenlab/`.
For the session in this example, the processed session data would be located at `/vol/cortex/cd4/geffenalb/processed_data/BH/AS20-minimal3/03112025/`.

For SpikeGlx recordings, this pipeline also looks for raw session data, for example in `/vol/cortex/cd4/geffenalb/raw_data/BH/AS20-minimal3/03112025/`

This pipeline writes Phy results into the session's analysis sibdirectory, for example `/vol/cortex/cd4/geffenalb/analysis/BH/AS20-minimal3/03112025/`

![Cortex remote desktop files view](./aind-ephys-pipeline-results.png)
