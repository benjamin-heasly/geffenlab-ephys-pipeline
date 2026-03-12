# Pipeline configs

The [AIND ephys pipeline](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline) and the Geffen lab's [phy-export](./phy-export/phy-export.nf) pipeline are both driven by [Nextflow config files](https://www.nextflow.io/docs/latest/config.html).

This doc should help you create a new config file, for example to support a new rig.  The same kind of config applies when you [run the AIND ephys pipeline](./run-aind-ephys-pipeline.md) and when you [run the Geffen lab phy-export pipeline](./run-phy-export.md).  This doc will focus on the [phy-export](./phy-export/phy-export.nf) pipeline.

# Existing config

The existing, default config file for the Geffen lab phy-export pipeline is here in this repo, at [phy-export/cortex.config](../phy-export/cortex.config).
When running the pipeline, you specify which config file to use, for example:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow geffenlab-ephys-pipeline/phy-export/phy-export.nf \
  --config geffenlab-ephys-pipeline/phy-export/cortex.config \          <--- specify the config file
  --experimenter BH \
  --subject AS20-minimal3 \
  --date 03112025 \
  --input spikeglx
```

# Create a custom pipeline config file

You can copy the default config file and make modifications to support your own rig or data.
This example copies the default phy-export pipeline config for the user `ben`.
You should use your own user name (or other distinctive name):

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/phy-export

cp cortex.config ben-cortex.config
```

# Edit your custom pipeline config file

Each config file has several sections like `params { ... }`, `process { ... }`, `docker { ... }`, `dag { ... }`, `report { ... }`, `timeline { ... }`, `trace { ... }`.  Most of these are needed to make the pipeline run on cortex, and you should leave them as-is.

The `params { ... }` section is the only section that you'll need to customize.  And -- many of the parameters in this section can also be left as-is.  The parameters to edit start around [line 38](../phy-export/cortex.config#L38).  As of writing they look like this:

```
    // Should CatGT look for Neuropixels plus NIDQ ('-ap -ni') or just Neuropixels ('-ap')?
    catgt_streams = '-ap -ni'

    // Should CatGT expect OneBox ('-obx=0') or not (empty '')?
    catgt_onebox = ''

    // Which event channels should CatGT try extract?
    catgt_events = '-xa=0,0,0,1,3,500 -xia=0,0,1,3,3,0 -xd=0,0,8,3,0 -xid=0,0,-1,2,1.7 -xid=0,0,-1,3,5'

    // Specify any other CatGT command arguments.
    // Since we're not using CatGT to filter the binary, we need -no_tshift.
    catgt_misc = '-no_tshift -prb_fld -out_prb_fld'

    // Our CatGT Python wrapper takes the --probe-id, --run, --gate, and --trigger as separate args.
    // All the other CatGT args go together here.
    catgt_args = "${params.catgt_streams} ${params.catgt_onebox} ${params.catgt_events} ${params.catgt_misc}"

    // What sync pulse period should TPrime expect?
    tprime_sync_period = 1.0

    // What stream of sync events should TPrime convert to?
    // This pattern must match a sync event .txt within the catgt/ output subdirectory.
    //  - To align to NIDQ use a pattern lile this: tprime_to_stream = "*/*nidq.xd_8_4_500.txt"
    //  - To align to a probe use a pattern lile this: tprime_to_stream = "*/*/*.imec0.ap.*.txt"
    tprime_to_stream = "*/*/*.imec0.ap.*.txt"

    // Which other event streams should TPrime convert to the stream above?
    // Each pattern below must match an event .txt within the catgt/ output subdirectory.
    // The patterns on the left are for events that should be converted.
    // The patterns on the right are for sync events on the same stream.
    tprime_from_map = [
        "*/*nidq.xa_0_500.txt": "*/*nidq.xd_8_4_500.txt",
        "*/*nidq.xia_1_0.txt": "*/*nidq.xd_8_4_500.txt",
        "*/*nidq.xd_8_3_0.txt": "*/*nidq.xd_8_4_500.txt",
        "*/*nidq.xid_8_2_1p7.txt": "*/*nidq.xd_8_4_500.txt",
        "*/*nidq.xid_8_3_5.txt": "*/*nidq.xd_8_4_500.txt",
    ]

    // Format these "from streams" in the way our TPrime Python wrapper expects.
    tprime_from_streams = params.tprime_from_map.collect { other, sync -> "${sync}:${other}" }.join(' ')

    // Our TPrime Python wrapper can convert sorted spike times in the Phy folder(s) as well.
    // Which text file(s) contains the probe sync events produced by CatGT?
    // This pattern must match sync event .txt within the catgt/ output subdirectory.
    tprime_phy_from_pattern = "*/*/*.ap.*.txt"

    // Choose a JSON file of parameters Bombcell.
    bombcell_params_file = "geffenlab-ephys-pipeline/phy-export/bombcell-params.json"
```

## CatGT params

You can edit the `catgt_` params to suit your SpikeGlx rig.  All of these are combined into one long string of arguments, `catgt_args`.  These are passed to CatGT when the pipeline runs.

## TPrime params

You can edit the `tprime_` params to suit your SpikeGlx rig, as well.  These are passed to our own [tprime.py](https://github.com/benjamin-heasly/geffenlab-spikeglx-tools/blob/main/code/tprime.py) wrapper script when the pipeline runs.  The wrapper is intended to make it easier to find and configure "from" and "to" mappings for multiple streams and event channels.  In turn, this wrapper script generates a long string of arguments to pass to TPrime itself.

`tprime_to_stream` should be a [glob](https://docs.python.org/3/library/glob.html) pattern.  It's used to search among the outpus of CatGT, to select the file of sync event times to which other event streams are aligned.  The default  `*/*/*.imec0.ap.*.txt` would match sync events for probe `imec0`.  A possible alternative `*/*nidq.xd_8_4_500.txt` might match NIDQ sync events.

`tprime_from_map` configures other event streams.  Each of these requires two glob patterns, separated by a colon `:`.
For example:

```
        "*/*nidq.xa_0_500.txt": "*/*nidq.xd_8_4_500.txt",
```

The glob on the left of each colon, like `*/*nidq.xa_0_500.txt`, selects interesting event times to be mapped.

The glob on the right of each colon, like `*/*nidq.xd_8_4_500.txt`, selects the sync events from the same stream.

All of these mappings are combined into a long line of arguments, `tprime_from_streams`, to pass to our `tprime.py` wrapper script.

Our `tprime.py` wrapper script can also convert sorted spike times for each probe, found in one or more Phy folders.  The paremeter `tprime_phy_from_pattern` is a glob pattern to match probe sync event files in the CatGT output folder.

## Bombcell params

Finally, `bombcell_params_file` specifies a file of Bombcell parameters to use during automated curation.  Bombcell accepts a large number of parameters, so these are stored in a separate file.

The default file is in this repo, [phy-export/bombcell-params.json](../phy-export/bombcell-params.json).  This is specified in the overall pipeline config file as:

```
    // Choose a JSON file of parameters Bombcell.
    bombcell_params_file = "geffenlab-ephys-pipeline/phy-export/bombcell-params.json"
```

The file path here is relative to our Nextflow working directory, `/vol/cortex/cd4/geffenlab/nextflow`.  This working directory is automatically set by our `run_pipeline.py` script.

Like the overall pipeline config file, you can copy and modify the Bombcell parameters file.

# Create a custom Bombcell parameters file

You can copy the default Bombcell parameters JSON file and make modifications to support your own rig or data.
This example copies the default parameters JSON file for the user `ben`.
You should use your own user name (or other distinctive name):

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/phy-export

cp bombcell-params.json ben-bombcell-params.json
```

# Edit your custom Bombcell parameters file

When the pipeline runs, our [Bombcell Python wrapper script](https://github.com/benjamin-heasly/geffenlab-bombcell/blob/main/code/run.py) will automatically set several Bombcell parameters based on the pipeline data:

 - `savePlots`
 - `plotsSaveDir`
 - `computeDistanceMetrics`
 - `ephys_sample_rate`
 - `nChannels`
 - `nSyncChannels`

You can omit these from your own JSON file.  If you do specify these, the values you specify will take precedence.

# Select your custom Bombcell parameters file

To select your custom Bombcell parameters file, edit the corresponding line or your overall pipeline config file.
For example:

```
    // Choose a JSON file of parameters Bombcell.
    bombcell_params_file = "geffenlab-ephys-pipeline/phy-export/ben-bombcell-params.json"
```

# Run with your custom pipeline config file

Now you can run a pipeline with your own, custom pipeline config and Bombcell parameters.
All you have to do is pass your own config file to the `run_pipeline.py` command.
For example:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow geffenlab-ephys-pipeline/phy-export/phy-export.nf \
  --config geffenlab-ephys-pipeline/phy-export/ben-cortex.config \          <--- your own config file
  --experimenter BH \
  --subject AS20-minimal3 \
  --date 03112025 \
  --input spikeglx
```

# Save customizations to this repo

It's a good idea to commit your custom pipeline config and Bombcell parameters JSON to this repository.
You should commit changes whenever you make them, so that you can keep track of changes over time, and reproduce config you might have used in the past.

Review your new files:

```
$ cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/phy-export

$ git status

On branch master
Your branch is up to date with 'origin/master'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	ben-bombcell-params.json
	ben-cortex.config
```

Commit your additions to the repo.

```
$ git add .
$ git status

On branch master
Your branch is up to date with 'origin/master'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   ben-bombcell-params.json
	new file:   ben-cortex.config

$ git commit -m "Add phy-export pipeline config and Bombcell parameters JSON for ben."

[master b0520c3] Add phy-export pipeline config and Bombcell parameters JSON for ben.
 2 files changed, 180 insertions(+)
 create mode 100644 phy-export/ben-bombcell-params.json
 create mode 100644 phy-export/ben-cortex.config
```

Push your new commit to GitHub.

```
git push
```

You will be prompted for a GitHub username and password.
You should [create a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic) and use the token, instead of your normal GitHub login password.

TODO: we'll need to manage GitHub contributors for this repo.  We might want to move it from [benjamin-heasly](https://github.com/benjamin-heasly?tab=repositories) to [geffenlab](https://github.com/geffenlab?tab=repositories).  In the meantime we can still run with custom config on cortex, and it'll be up to ben to push changes.
