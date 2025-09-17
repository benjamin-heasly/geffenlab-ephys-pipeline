# Pipeline Configurations

This document describes ways to configure existing pipelines to work with different experiment configurations or on different machines.

This follows on from our other docs [cortex user setup](./cortex-user-setup.md) and [cortex first run](./cortex-first-run.md).  Those used generic "cortex" configurations for the AIND ephys pipeline and for the Geffen Lab ephys pipeline.  These are good for getting started.  Read on for additional configuration options.

# AIND ephys pipeline

We can configure Nextflow pipelines using configuration files.  For the AIND ephys pipeline our default configuration file is [aind-ephys-pipeline/cortex.config](./aind-ephys-pipeline/cortex.config).

To modify the configuration for a given machine or experiment setup, make a copy of this file and modify it.  Commit your copy to this repo and push to GitHub, to allow yourself and others to track and re-run this new configuration.

To run the AIND ephys pipeline with your new configuration, pass your new file name on the Nextflow command line using `-C`.  For example:

```
NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/aind-ephys-pipeline/my_config.config \            <-- config file with -C
  run aind-ephys-pipeline/pipeline/main_multi_backend.nf
```

## What's configurable

The config file [aind-ephys-pipeline/cortex.config](./aind-ephys-pipeline/cortex.config) itself is the source of truth for what's configurable, and the coments there in the `params` section should explain these options.  We can call out a few below that might be of most interest.

### Select a `gpu_device`

Depending on the current processing load on cortex, you might need to select a specific GPU device.  You can look at GPU device status by running `nvidia-smi`.  You can list GPU devices and their unique IDs with `nvidia-smi -L`.

You can edit `gpu_device` in the config file to specify which GPU to use by default.  You can also pass a value for `--gpu_device` on the Nextflow command line.

```
NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/aind-ephys-pipeline/my_config.config \
  run aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --gpu_device 2                                                                <-- GPU device param
```

### Spike sorting args.

The AIND ephys pipeline accepts a full list of parameters to pass to Kilosort4.  The parameters themselves are described in the [Kilosort4 docs](https://kilosort.readthedocs.io/en/latest/README.html).

To change Kilosort4 parameters, edit the value of `spikesorting_args` in your config file.  This value is a multiline block of JSON text.  It's probably best to just edit specific parameter values, and not to restructure this block of text.

# Geffen lab ephys pipeline

The original is [pipeline/cortex.config](./pipeline/cortex.config).  Copy this and modify it for your machine and/or data.  Commit and push your copy of the modified file to this repo on GitHub, so that you and others can run the pipeline again with the same configuration

Then when running the AIND ephys pipeline use the `-C` option to specify your own config file.  For example:

```
cd /vol/cortex/cd4/geffenlab/nextflow
conda activate geffen-pipelines

NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/pipeline/my_config.config \                        <-- your config file with -C
  run geffenlab-ephys-pipeline/pipeline/main.nf \
  --subject AS20-minimal2 \
  --date 03112025
```

GatGT args

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
