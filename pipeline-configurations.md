# Pipeline Configurations

This document describes how to configure our pipelines to work with different experiment setups.

This follows on from other docs [cortex user setup](./cortex-user-setup.md) and [cortex first run](./cortex-first-run.md).  Those used generic configurations for the AIND ephys pipeline and Geffen Lab ephys pipeline.  These are good for getting started, but read on for more options.

# AIND ephys pipeline

The AIND ephys pipeline does recording preprocessing, spike sorting, and automated curation.  This is all based on SpikeInterface and Kilosort.

We use two configuration files for the AIND ephys pipeline:
 - a Nextflow `.config` file for the pipeline itself, like [aind-ephys-pipeline/cortex.config](./aind-ephys-pipeline/cortex.config)
 - a parameters JSON file for individual SpikeInterface and Kilosort steps, like [aind-ephys-pipeline/spikeglx-ks4-default.json](./aind-ephys-pipeline/spikeglx-ks4-default.json)

To make new configurations, copy and modify one or both of these files.  Commit copies to this repository and push to GitHub, so that you and others can track, reference, and reuse each configuration.

## AIND nextflow `.config` file

When running the AIND pipeline, specify your Nextflow `.config` file as the `--config` argument to [run_pipeline.py](./scripts/run_pipeline.py).  For example:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --config geffenlab-ephys-pipeline/aind-ephys-pipeline/my-aind-configuration.config \
  ...
```

### Choose a parameters JSON file

Within your AIND Nextflow `.config` file you can edit `params_file` to specify a parameters JSON file for SpikeInterface and Kilosort.

You can also pass a value for `--params_file` on the command line.  Extra parameters like this will be passed on to Nextflow and the pipeline.  For example:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --config geffenlab-ephys-pipeline/aind-ephys-pipeline/my-aind-configuration.config \
  --params_file geffenlab-ephys-pipeline/aind-ephys-pipeline/my-parameters.json \
  ...
```

### Choose a Kilosort `gpu_device`

Depending on the current processing load on cortex, you might need to select a specific GPU device.  You can look at GPU device load by running `nvidia-smi`.  You can list GPU devices and their unique UUIDs with `nvidia-smi -L`.

You can specify a default `gpu_device` within your Nextflow `.config` file.  You can also pass a value for `--gpu_device` on the command line.  For example:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --config geffenlab-ephys-pipeline/aind-ephys-pipeline/my-aind-configuration.config \
  --params_file geffenlab-ephys-pipeline/aind-ephys-pipeline/my-parameters.json \
  --gpu_device 2 \
  ...
```

## Parameters JSON file

The AIND pipeline parameters JSON file contains many parameters for preprocessing, spike sorting, postprocessing, and automated curation.  It's a large file, but here are some tips.

### Documentation

The AIND ephys pipeline repo [README](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline/blob/6e805354e428ff8e935750bb5bbe604847a5f0f9/README.md) links to documentation for each step, including what parameters are available.  These should correspond with the parameters JSON file.

For SpikeInterface steps, the [SpikeInterface docs](https://spikeinterface.readthedocs.io/en/stable/) should describe what the different parameters do.  The [Kilosort4 docs](https://kilosort.readthedocs.io/en/latest/parameters.html) describe several of its parameters and also link to the code for further comments.

### Original

The original, default JSON parameters file comes from the AIND ephys pipeline repo, specifically at revision `6e805354e428ff8e935750bb5bbe604847a5f0f9` from 4 June 2025: [default_params.json](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline/blob/6e805354e428ff8e935750bb5bbe604847a5f0f9/pipeline/default_params.json).

Our copy, [aind-ephys-pipeline/spikeglx-ks4-default.json](./aind-ephys-pipeline/spikeglx-ks4-default.json), modifies this in two ways:
 - In the `job_dispatch` section, `input` format defaults to `spikeglx`. 
 - In the `nwb` section, `skip_lfp` defaults to `true`.
 - In the `preprocessing` section, `min_preprocessing_duration` defaults to `20` (enables testing with short recordings).

### Brain-region-specific parameters

You might create alternative parameters JSON files for different brain regions.  Region-specific parameters might be:
 - `refractory_period_ms` in the `postprocessing` section
 - `Th_universal` in the `spikesorting` section
 - `Th_learned` in the `spikesorting` section

### Filtering / de-noising the recordings

The AIND ephys pipline does filtering / de-noising of recordings (we won't use CatGT for this purpose).  The filtering happens during the [preprocessing](https://github.com/AllenNeuralDynamics/aind-ephys-preprocessing/?tab=readme-ov-file#parameters) step.  The relevant parameter seems to be:
 - `denoising_strategy` in the `preprocessing` section

# Geffen lab ephys pipeline

The Geffen lab ephys pipeline runs after the AIND ephys pipeline.  It allows manual curation with Phy and aligns neural and behavior data to produce a reduced dataset and summary plots. 

We use one configuration files for the Geffen lab ephys pipeline:
 - a Nextflow `.config` file for the pipeline itself and for individual steps, like [pipeline/cortex.config](./pipeline/cortex.config)

To make new configurations, copy and modify this file.  Commit copies to this repository and push to GitHub, so that you and others can track, reference, and reuse each configuration.

## Geffen lab nextflow `.config` file

When running the Geffen lab pipeline, specify your Nextflow `.config` file as the `--config` argument to [run_pipeline.py](./scripts/run_pipeline.py).  For example:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow geffenlab-ephys-pipeline/pipeline/main.nf \
  --config geffenlab-ephys-pipeline/pipeline/my-geffen-config.config \
  ...
```

### CatGT arguments

For SpikeGLX rigs, we run CatGT to extract event times from data streams.  Since already did spike sorting in the AIND ephys pipeline, we only need it to extract events -- we don't need CatGT to filter the raw recording binary.

Our [pipeline/cortex.config](./pipeline/cortex.config) has several parameters starting with `catgt_` that you can edit to suit your experiment setup.  For example, you can edit `catgt_events` to configure the events for CatGT to extract.

These same parameters can be specified from the command line.  For example, you can pass values for `--catgt_run`, `--catgt_gate`, and `--catgt_trigger`:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow geffenlab-ephys-pipeline/pipeline/main.nf \
  --config geffenlab-ephys-pipeline/pipeline/my-geffen-config.config \
  --catgt_run 'AS20_03112025_trainingSingle6Tone2024_Snk3.1' \
  --catgt_gate 0 \
  --catgt_trigger 0 \
  ...
```

### TPrime arguments

For SpikeGLX rigs we also use TPrime to align event times between data streams / clocks.

Our [pipeline/cortex.config](./pipeline/cortex.config) has several parameters starting with `tprime_` that you can edit to suit your experiment setup.

Most of these, like `tprime_to_stream` and `tprime_from_map` use patterns to match event `.txt` files produced by CatGT.


### Synthesis

Our synthesis step creates an `events.csv` file in the Phy folder.  The event times in this file come from one of the adjusted event `.txt` files produced by TPrime.

To choose which event `.txt` file, edit `synthesis_event_times_pattern` in our [pipeline/cortex.config](./pipeline/cortex.config).
