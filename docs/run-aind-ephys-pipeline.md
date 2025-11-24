# Run AIND ephys pipeline

This doc should help you run the [AIND ephys pipeline](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline) for spike sorting and quality metrics.

Before running this you'll need to do one-time [cortex user setup](./cortex-user-setup.md) for your cortex user account and local lab machine.

You'll also need to [upload-data](./upload-data.md) for your session to cortex.

## run_pipeline.py

We use the [AIND ephys pipeline](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline) Nextflow code as-is.

We combine this with our own Nextflow configuration file which tells Nextflow to do things like:
 - Share CPU, GPU, and RAM with other cortex users.
 - Locate Geffen lab data and results within `/vol/cortex/cd4/geffenlab/`

To run the pipeline use our Python script [run_pipeline.py](./scripts/run_pipeline.py).  This script calls `nextflow run` for the pipeline itself, and also saves detailed logs within the results directory for each session.
We tell the script which pipeline to run with the `--workflow` argument.  We specifiy the configuration with `--config`.  We also pass the `experimenter`, `--subject`, and `--date` for the session we want to process.

The `--input` parameter can be `spikeglx` or `openephys`, to tell the AIND pipeline what kind of data to read.

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --config geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config \
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

## results

