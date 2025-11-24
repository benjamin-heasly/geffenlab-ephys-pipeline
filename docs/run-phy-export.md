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

We tell the script which pipeline to run with the `--workflow` argument.  We specifiy the configuration to use with `--config`.  We also pass the `--experimenter`, `--subject`, and `--date` for the session we want to process.

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
2025-11-24 13:02:06,751 [INFO] Completed at: 24-Nov-2025 13:02:06
2025-11-24 13:02:06,751 [INFO] Duration    : 8m 28s
2025-11-24 13:02:06,751 [INFO] CPU hours   : 0.4
2025-11-24 13:02:06,751 [INFO] Succeeded   : 4
```

## Results overview

The pipeline looks for processed session data within the lab's sotrage directory, `/vol/cortex/cd4/geffenlab/`.
For the session in this example, the processed session data would be located at `/vol/cortex/cd4/geffenalb/processed_data/BH/AS20-minimal3/03112025/`.
For SpikeGlx recordings, the pipeline also looks for raw session data, for example in `/vol/cortex/cd4/geffenalb/raw_data/BH/AS20-minimal3/03112025/`

The pipeline writes Phy results into the session's analysis subdirectory, for example `/vol/cortex/cd4/geffenalb/analysis/BH/AS20-minimal3/03112025/`

![Cortex remote desktop files view](./phy-export-results.png)

The pipeline may produce multiple subdirectories of Phy results, each with its own `params.py` and other `.tsv` and `.npy` files.
These may should distinguished by their probe id, like `imec0`, and recording number, like `recording1`.

Even for the same probe and recording, there can be multiple Phy subdirectories, from different stages of processing:

 - `phy-export/exported/phy/block0_imec0.ap_recording1/params.py`: initial export from AIND ephys pipeline, Kilosort, and SpikeInterface
 - `phy-export/tprime/phy/block0_imec0.ap_recording1/params.py`: for SpikeGlx recordings, with spike times adjusted by TPrime
 - `phy-export/bombcell/phy/block0_imec0.ap_recording1/params.py`: with automated curation and diagnostic plots by bombcell

The pipeline doesn't implement bombcell yet!
When it does we should prefer the results within `phy-export/bombcell/phy/`.
