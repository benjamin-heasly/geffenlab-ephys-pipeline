# Pipeline Configurations

This document describes ways to configure existing pipelines to work with different experiment configurations.

This follows on from other docs [cortex user setup](./cortex-user-setup.md) and [cortex first run](./cortex-first-run.md).  Those used generic configurations for the AIND ephys pipeline and Geffen Lab ephys pipeline.  These are good for getting started, read on for additional configuration options.

# AIND ephys pipeline

We use two configuration files for the AIND ephys pipeline:
 - a Nextflow `.config` file for the pipeline itself, like [aind-ephys-pipeline/cortex.config](./aind-ephys-pipeline/cortex.config)
 - a parameters JSON file for individual SpikeInterface and Kilosort steps, like [aind-ephys-pipeline/spikeglx-ks4-default.json](./aind-ephys-pipeline/spikeglx-ks4-default.json)

To make new configurations, copy and modify one or both of these files.  Commit copies to this repository and push to GitHub, so that you and others can track, reference, and reuse each configuration.

## AIND nextflow `.config` file

When running the AIND pipeline, specify your Nextflow `.config` file on the command line using using `-C`.  For example:

```
NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/aind-ephys-pipeline/my-configuration.config \
  run aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  # ...etc...
```

### Choose a `params_file`

You can specify a default JSON `params_file` within your Nextflow `.config` file.  You can also pass a value for `--params_file` on the Nextflow command line.  For example:

```
NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/aind-ephys-pipeline/my-configuration.config \
  run aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --params_file geffenlab-ephys-pipeline/aind-ephys-pipeline/my-parameters.json \
  # ...etc...
```

### Choose a `gpu_device`

Depending on the current processing load on cortex, you might need to select a specific GPU device.  You can look at GPU device load by running `nvidia-smi`.  You can list GPU devices and their unique UUIDs with `nvidia-smi -L`.

You can specify a default `gpu_device` within your Nextflow `.config` file.  You can also pass a value for `--gpu_device` on the Nextflow command line.  For example:

```
NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/aind-ephys-pipeline/my-configuration.config \
  run aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --params_file geffenlab-ephys-pipeline/aind-ephys-pipeline/my-parameters.json \
  --gpu_device 2
  # ...etc...
```

## Parameters JSON

The AIND pipeline parameters JSON file contains many parameters for preprocessing, spike sorting, and postprocessing and automated curation.  Here are some highlights.

### Documentation

The AIND ephys pipeline repo [README](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline/blob/6e805354e428ff8e935750bb5bbe604847a5f0f9/README.md) links to documentation for each step, including what parameters are available.

For SpikeInterface steps, the [SpikeInterface docs](https://spikeinterface.readthedocs.io/en/stable/) may describe what the different parameters do.  The [Kilosort4 docs](https://kilosort.readthedocs.io/en/latest/parameters.html) describe several of its parameters and also link to the code for further comments.

### Original

The original, default JSON parameters file comes from the AIND ephys pipeline repo, specifically at revision `6e805354e428ff8e935750bb5bbe604847a5f0f9` from 4 June 2025: [default_params.json](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline/blob/6e805354e428ff8e935750bb5bbe604847a5f0f9/pipeline/default_params.json).

Our copy, [aind-ephys-pipeline/spikeglx-ks4-default.json](./aind-ephys-pipeline/spikeglx-ks4-default.json), modifies this in two ways:
 - `input` format defaults to `spikeglx` in the `job_dispatch` section
 - `skip_lfp` defaults to `true` in the `nwb` section
 - `min_preprocessing_duration` defaults to `20` in the `preprocessing` section (allows processing shorter test data)

### Brain-region-specific parameters

You might create alternative parameters JSON files for different brain regions.  Region-specific parameters might be:
 - `refractory_period_ms` in the `postprocessing` section
 - `Th_universal` in the `spikesorting` section
 - `Th_learned` in the `spikesorting` section

### Filtering / de-noising the recordings

The AIND ephys pipline does filtering / de-noising of recordings (we won't use CatGT for this purpose).  The filtering happens during the [preprocessing](https://github.com/AllenNeuralDynamics/aind-ephys-preprocessing/?tab=readme-ov-file#parameters) step.  The relevant parameter seems to be:
 - `denoising_strategy` in the `preprocessing` section

# Geffen lab ephys pipeline

We only need one configuration files for the Geffen lab ephys pipeline:
 - a Nextflow `.config` file for the pipeline itself and for individual steps, like [pipeline/cortex.config](./pipeline/cortex.config)

To make new configurations, copy and modify this file.  Commit copies to this repository and push to GitHub, so that you and others can track, reference, and reuse each configuration.

## Geffen lab nextflow `.config` file

When running the Geffen lab pipeline, specify your Nextflow `.config` file on the command line using using `-C`.  For example:

```
NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/pipeline/my_config.config \
  run geffenlab-ephys-pipeline/pipeline/main.nf \
  # ...etc...
```

## Work in Progress below...

### CatGT

For SpikeGLX rigs, we need to configure CatGT.
We could ask for one giant command string, or break this up into parts.

 - probe_id imec0
 - spike_glx_gate 0
 - spike_glx_trigger 0
 - spike_glx_run AS20_03112025_trainingSingle6Tone2024_Snk3.1
 - streams -ap -ni, (-ni optional)
 - onebox -obx=0 (optional)
 - events to extract '-xa=0,0,0,1,3,500 -xia=0,0,1,3,3,0 -xd=0,0,8,3,0 -xid=0,0,-1,2,1.7 -xid=0,0,-1,3,5'

Since we're not filtering the binary, we also need
 - -no_tshift

Misc
 - -prb_fld -out_prb_fld

### TPrime

For SpikeGLX rigs, we need to configure TPrime.
This is easier to break into parts and give to our Python wrapper

 - --sync_period 1.0
 - --probe-id imec0
 - --to-stream based on --probe-id
 - --phy-from-stream based on --probe-id
 - events sync_pattern:event_pattern
    **/*nidq.xd_8_4_500.txt:**/*nidq.xa_0_500.txt \
    **/*nidq.xd_8_4_500.txt:**/*nidq.xia_1_0.txt \
    **/*nidq.xd_8_4_500.txt:**/*nidq.xd_8_3_0.txt \
    **/*nidq.xd_8_4_500.txt:**/*nidq.xid_8_2_1p7.txt \
    **/*nidq.xd_8_4_500.txt:**/*nidq.xid_8_3_5.txt \

### Synthesis

Our synthesis step copies events from one source into an "events.csv" for Phy and downstream analysis.

 - event_pattern **/*nidq.xd_8_3_0.txt
