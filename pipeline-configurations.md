# Pipeline Configurations

This document describes ways to configure existing pipelines to work with different experiment configurations or on different machines.

This follows on from our other docs [cortex user setup](./cortex-user-setup.md) and [cortex first run](./cortex-first-run.md).  Those used generic "cortex" configurations for the AIND ephys pipeline and for the Geffen Lab ephys pipeline.  These are good for getting started.  Read on for additional configuration options.

# AIND ephys pipeline

We can configure Nextflow pipelines using configuration files.  For the AIND ephys pipeline our default configuration file is [aind-ephys-pipeline/cortex.config](./aind-ephys-pipeline/cortex.config).

To modify the configuration for a given machine or experiment setup, make a copy of this file and modify it.  Commit your copy to this repo and push to GitHub, so that you and others can track and re-run with the same configuration.

To run the AIND ephys pipeline with your new configuration, pass your new file name on the Nextflow command line using `-C`.  For example:

```
NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/aind-ephys-pipeline/my_config.config \    <-- specify your config file with -C
  run aind-ephys-pipeline/pipeline/main_multi_backend.nf
  # ...etc...
```

## What's configurable

The config file [aind-ephys-pipeline/cortex.config](./aind-ephys-pipeline/cortex.config) itself is the source of truth for what's configurable, and the coments there in the `params` section should explain these options.  I'll call out a few of these below.

### Select a `gpu_device`

Depending on the current processing load on cortex, you might need to select a specific GPU device.  You can look at GPU device status by running `nvidia-smi`.  You can list GPU devices and their unique IDs with `nvidia-smi -L`.

You can edit `gpu_device` in the config file to specify which GPU to use by default.  You can also pass a value for `--gpu_device` on the Nextflow command line.

```
NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/aind-ephys-pipeline/my_config.config \
  run aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --gpu_device 2
  # ...etc...
```

### Spike sorting and postprocessing args

The AIND ephys pipeline accepts many parameters for spike sorting with Kilosort4 and postprocessing with SpikeInterface.  The parameters themselves are described in the [Kilosort4 docs](https://kilosort.readthedocs.io/en/latest/README.html) and [SpikeInterface postprocessing docs](https://spikeinterface.readthedocs.io/en/stable/modules/postprocessing.html).

Some of these parameters can be set in groups, per brain area, including the expected refractory period in ms and the thresholds Kilosort4 uses during sorting.  To choose a parameter group you can edit `brain_region` in the config file.  You can also pass a value for `--brain_region` on the Nextflow command line.

```
NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/aind-ephys-pipeline/my_config.config \
  run aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --brain_region medulla
  # ...etc...
```

You can edit many additional parameters in your config file, within `spikesorting_args` or `postprocessing_args`.  Each of these is a multiline block of JSON text.  The block formatting matters, so it would be best to edit specific parameter values and not change the overall structure.  The default values we have here came from the AIND ephys pipeline [default_params.json](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline/blob/main/pipeline/default_params.json).


# Geffen lab ephys pipeline

For the Geffen lab ephys pipeline our default configuration file is [./pipeline/cortex.config](./pipeline/cortex.config).

To modify the configuration for a given machine or experiment setup, make a copy of this file and modify it.  Commit your copy to this repo and push to GitHub, so that you and others can track and re-run with the same configuration.

To run the Geffen lab ephys pipeline with your new configuration, pass your new file name on the Nextflow command line using `-C`.  For example:

```
cd /vol/cortex/cd4/geffenlab/nextflow
conda activate geffen-pipelines

NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/pipeline/my_config.config \               <-- specify your config file with -C
  run geffenlab-ephys-pipeline/pipeline/main.nf \
  # ...etc...
```

## Work in progress below :-)

CatGT args

probe_id imec0
spike_glx_gate 0
spike_glx_trigger 0
spike_glx_run AS20_03112025_trainingSingle6Tone2024_Snk3.1
cat_gt_args -ni -ap -prb_fld -out_prb_fld -no_tshift -xa=0,0,0,1,3,500 -xia=0,0,1,3,3,0 -xd=0,0,8,3,0 -xid=0,0,-1,2,1.7 -xid=0,0,-1,3,5

TPrime args

sync_period 1.0
probe_id imec0
    --to-stream and --phy-from-stream based on short probe_id
tprime_streams
    **/*nidq.xd_8_4_500.txt:**/*nidq.xa_0_500.txt \
    **/*nidq.xd_8_4_500.txt:**/*nidq.xia_1_0.txt \
    **/*nidq.xd_8_4_500.txt:**/*nidq.xd_8_3_0.txt \
    **/*nidq.xd_8_4_500.txt:**/*nidq.xid_8_2_1p7.txt \
    **/*nidq.xd_8_4_500.txt:**/*nidq.xid_8_3_5.txt \
