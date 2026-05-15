# Run Proceed

This document should help you run a processing pipeline using [Proceed](https://benjamin-heasly.github.io/proceed/) along with one of the lab's [pipeline definition YAML files](../proceed/).

Before running this you should do initial [cortex-user-setup.md](./cortex-user-setup.md).

# Test with small dataset

This seciton shows how to do a full pipeline run with a small dataset.
Run the commands below from a terminal on cortex (see [cortex-remote-desktop-connection](./cortex-user-setup.md#cortex-remote-desktop-connection)).

First, remove outputs from any previous test runs.

```
rm -rf /vol/cortex/cd5/geffenlab/processed_data/BH/AS20-demo/03112025/
rm -rf /vol/cortex/cd5/geffenlab/analysis/BH/AS20-demo/03112025/
```

The small, `AS20-demo` dataset came from a SpikeGLX-plus-NIDQ rig.
Our [as-nidq.yaml](../proceed/as-nidq.yaml) is a good fit for processing it.

Use the `proceed run` command and specify:
 - `proceed/as-nidq.yaml` for the pipeline definition
 - several `args` for the experimenter (`BH`), subject (`AS20-demo`), and date (`03112025`)

```
# Use our conda environment with Python, etc.
conda activate geffen-pipelines

cd ~/geffenlab-ephys-pipeline
proceed run proceed/as-nidq.yaml --args experimenter=BH subject=AS20-demo date="03112025"
```

For the samll dataset, processing should take about 5-10 minutes to complete.

## raw data inputs

The pipeline will look for raw data within a subfolder of `/vol/cortex/cd5/geffenlab/raw_data`.  It will expect data to use a standard directory structure based on experimenter, subject and date -- as in [upload-data.md](./upload-data.md).

![Ubuntu Files view of a raw_data/ subdirectory containing behavioral and neural data](./cortex-data.png)

## logging outputs

Proceed will print a lot of logging information to the console.
It will also save the same logging information, and more, in a `proceed_out` subdirectory of the current working directory.  This will contain logs organized by pipeline name, date, and step name.

![Ubuntu Files view of a proceed_out/ directory containing processing logs](./proceed_out.png)

## processed data and analysis outputs

The pipeline writes intermediate processing results into a subdirectory of `/vol/cortex/cd5/geffenlab/processed_data`, with results organized by experimenter, subject, date, step name, SpikeGLX run, and probe.

![Ubuntu Files view of a processed_data/ subdirectory containing intermediate processing results](./processed_data.png)

It also writes final, summarized results into a subdirectory of `/vol/cortex/cd5/geffenlab/analysis`, with results organized by experimenter, subject, date, SpikeGLX run, and probe.

![Ubuntu Files view of an analysis/ subdirectory containing final, summarized processing results](./analysis.png)

# Run with full datasets

The pipeline can run on full datasets as well, with the same overall flow of inputs and outpus.
See [upload-data.md](./upload-data.md) to get you full dataset on cortex.

You'll need to select a pipeline definition YAML file that's suitable for your data.
As of writing we have two:
 - [as-nidq.yaml](../proceed/as-nidq.yaml) is a good fit for a SpikeGLX-plus-NIDQ rig.
 - [ad-onebox.yaml](../proceed/ad-onebox.yaml) is a good fit for a SpikeGLX-plus-OneBox rig with a continuous treadmill signal.

Here are some examples of running full SpikeGLX-plus-NIDQ sessions.

```
conda activate geffen-pipelines
cd ~/geffenlab-ephys-pipeline

# single-probe NIDQ session
proceed run proceed/as-nidq.yaml --args experimenter=AS subject=AS20 date="03112025"

# dual-probe NIDQ session
proceed run proceed/as-nidq.yaml --args experimenter=AS subject=AS40 date="01062026"
```

Here are some examples of running full SpikeGLX-plus-OneBox sessions.

```
conda activate geffen-pipelines
cd ~/geffenlab-ephys-pipeline

# longer sessions with OneBox and treadmill continuous signal
proceed run proceed/ad-onebox.yaml --args experimenter=AD subject=AD025 date="03102026"
proceed run proceed/ad-onebox.yaml --args experimenter=AD subject=AD025 date="03112026"
```

These procesing runs may take a few hours to complete.

## Configuring pipelines

Please see [pipeline-config.md](./pipeline-config.md) for more details about how to configure various pipeline options.
For a new rig, it might be that you can reuse an existing pipeline, and only have to specify a few rig-specific specific parameters like CatGT or TPrime arguments, or probe-specific parameters for Kilosort4 or Bombcell.

# Reprocessing a datset

You can re-run a pipeline on the same dataset.
This could be useful if you want to run a new version of the pipeline or an individual step.

Reprocessing might also be useful if you modify some of the intermediate data, for example during interactive curation with Phy (see [run-phy.md](./run-phy.md)).

Here are a few ways to reprocess a dataset.

## erase and start fresh

At the most extreme, you can delete old processing results and run everything fresh.
For example with experimenter `BH`, subject `AS20-demo`, and date `03112025`, you could remove all pipeline outputs like this:

```
rm -rf /vol/cortex/cd5/geffenlab/processed_data/BH/AS20-demo/03112025/
rm -rf /vol/cortex/cd5/geffenlab/analysis/BH/AS20-demo/03112025/
```

Use caution when deleting files!

## overwrite old results with `--force-rerun`

You can also re-run a pipeline and let it overwrite old processing results.

For example:

```
conda activate geffen-pipelines
cd ~/geffenlab-ephys-pipeline

proceed run proceed/as-nidq.yaml --args experimenter=BH subject=AS20-demo date="03112025" --force-rerun
```

Note the `--force-rerun` flag passed to `proceed run`.
Normally Proceed will keep track of which steps have already completed, for a given dataset, and it will skip those steps on subsequent runs.
Passing `--force-rerun` tells Proceed to always re-run completed steps.

## run specific steps with `--step-names`

You can also ask proceed to re-run specific pipeline steps, instead of starting from the beginning.

For example:

```
conda activate geffen-pipelines
cd ~/geffenlab-ephys-pipeline

proceed run proceed/as-nidq.yaml --args experimenter=BH subject=AS20-demo date="03112025" --force-rerun --step-names bombcell summary
```

The arguments `--step-names bombcell summary` tell proceed to run only two steps: `bombcell` and `summary`.  This assumes previous steps have already completed.

Rerunning steps like these might be useful following interactive curation with Phy (see [run-phy.md](./run-phy.md)).

The names of the steps are declared in each pipeline YAML file.
Each block of text in the `steps:` section of the YAML begins with a name, like `- name: bombcell` or `- name: summary`.

# Scripting batches of multiple datasets

Each of our pipeline runs is focused on processing one dataset at a time, for a given experimenter, subject, and date.
But you can use a script to process multiple datasets in an unattended batch.

## handling disconnections and network interruptions

When running long batches make sure that you can disconnect your local machine and reconnect later, without interrupting the processing.
There are a few good ways to do this:
 - connect via remote desktop, as in [cortex-remote-desktop-connection](./cortex-user-setup.md#cortex-remote-desktop-connection)
 - connect via `ssh` and use [tmux](https://github.com/tmux/tmux/wiki)
 - connect via `ssh` and use [screen](https://www.gnu.org/software/screen/manual/screen.html)

If you don't do one of these then a network interruption, or just turning off your local machine (eg to go home) would cause processing to stop -- and that would defeat the goal of running long batches!

## shell scripting

A plain old shell script is one way to script up a batch.
You can put multiple `proceed run ...` calls in a shell script and run this from the terminal.

For example, you could save the following script as `my-proceed-batch.sh` in your home folder on cortex:

```shell
#!/bin/sh

# Process two or more sessions.
proceed run ~/geffenlab-ephys-pipeline/proceed/as-nidq.yaml --args experimenter=BH subject=AS20-demo date="03112025"
proceed run ~/geffenlab-ephys-pipeline/proceed/as-nidq.yaml --args experimenter=BH subject=AS20-minimal3-plus date="03112025"
```

Then you could run the script from a cortex terminal:

```shell
conda activate geffen-pipelines

cd ~

chmod +x my-proceed-batch.sh
./my-proceed-batch.sh
```

This should work and it might be be all you need.
On the other hand, it might not be robust in case of errors.

## Python scripting

Alternatively, you can call proceed via a Python script.
This might make it easier to organize parameters and handle errors.

For example, you could save the following script as `my-proceed-batch.py` in your home folder on cortex:

```python
import logging
import sys

from proceed.cli import main


# Enable formatted console logging for this script.
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Choose which pipeline to run.
pipeline_yaml = "geffenlab-ephys-pipeline/proceed/as-nidq.yaml"

# Choose datasets to process as (experimenter, subject, date).
datasets = [
    ("BH", "AS20-demo", "03112025"),
    ("BH", "AS20-minimal3-plus", "03112025"),
]

logging.info(f"Processing {len(datasets)} datasets.")

# Process each dataset and collect exceptions as (dataset, exception).
exceptions = []
for index, dataset in enumerate(datasets):
    try:
        logging.info(f"Starting on dataset {index + 1}/{len(datasets)}: {dataset}\n")

        # Call proceed -- this is equivalent to "proceed run ..." from the command line.
        # You could add other command line arguments here, including --force-rerun or --step-names.
        (experimenter, subject, date) = dataset
        proceed_args = [
            "run", pipeline_yaml,
            "--args", f"experimenter={experimenter}", f"subject={subject}", f"date={date}"
        ]
        exit_code = main(proceed_args)

        if exit_code != 0:
            raise ValueError(f"Proceed gave nonzero exit code {exit_code}, please see logs in proceed_out/")

        logging.info(f"Finished dataset {index + 1}/{len(datasets)}: {dataset}\n")

    except Exception as e:
        logging.error(f"Error processing dataset {index + 1}/{len(datasets)}: {dataset}:")
        logging.error(f"{e}\n")
        exceptions.append((dataset, e))

# How did it go?
logging.info(f"Done processing {len(datasets)} datasets.")
if exceptions:
    logging.error(f"{len(exceptions)} datasets had errors:\n")
    for (dataset, e) in exceptions:
        logging.error(f"For dataset {dataset}:")
        logging.error(f"{e}\n")
else:
    logging.info("No errors detected.")
```

Then you could run the Python script from a cortex terminal:

```shell
conda activate geffen-pipelines

cd ~

python my-proceed-batch.py
```

The Python `try:` block will trap errors during processing, including errors in the script itself and errors reported by Proceed.
The script will collect errors as they come, move on to the next dataset, and summarize any errors at the end.

## reviewing batch results

At the end of a long processing batch you can review results printed in the console.
This might be a lot of text.

You can also see results broken down by processing run and by step, in the `proceed_out/` subdir of your current directory.
Proceed writes logs and other outputs into this subdir whenever it runs.
The logs are organized by pipeline name, processing date-time, and step name.

![Ubuntu Files view of a proceed_out/ directory containing processing logs](./proceed_out.png)

It might be easier to review these one at a time, especially in case of errors.
