# Cortex First Run

This doc should help with your first pipeline run on cortex, using some known data.

Before running pipelines you'll need to do some one-time [cortex user setup](./cortex-user-setup.md) for your cortex user account and local lab machine.

The instructions below show how to process lab data using the [AIND ephys pipeline](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline) for spike sorting and quality metrics, and the [Geffen lab ephys pipeline](https://github.com/benjamin-heasly/geffenlab-ephys-pipeline) for combining data modalities and producing summary figures.

# Data locations

Before processing we need to put the data on cortex.  Geffen lab data have been assigned to a specific directory on cortex:

```
/vol/cortex/cd4/geffenlab/
```

Raw, original rig data should go into a `raw_data/` subdirectory of this storage directory.

```
/vol/cortex/cd4/geffenlab/raw_data/
```

Within this `raw_data/` subdirectory we can orgaize files by experimenter initials, subject, date, and data modality.

For example we have a minimal testing dataset that uses the following:
 - experimenter: `BH`
 - subject: `AS20-minimal3`
 - date: `03112025`
 - modalities: `behavior` and `ecephys`

Here's the minimal testing dataset at a glance:

```
/vol/cortex/cd4/geffenlab/
└── raw_data/
    └── BH/
        └── AS20-minimal3/
            └── 03112025/
                ├── behavior/
                │   ├── AS20_031125_trainingSingle6Tone2024_0_39.mat
                │   └── AS20_031125_trainingSingle6Tone2024_0_39.txt
                └── ecephys/
                    └── AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/
                        ├── AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.meta
                        ├── AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.bin
                        └── AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/
                            ├── AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.bin
                            └── AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.meta
```

The subject id `AS20-minimal3` is unusual.  It means the original data are from subject `AS20`, but for testing we created a smaller version of the dataset (just a few trials) using tools in [geffenlab-minimal-data](https://github.com/benjamin-heasly/geffenlab-minimal-data).

# Process the `AS20-minimal3` dataset

Let's start by processing a small testing dataset for subject `AS20-minimal3`.  This processing run should only take a few minutes.

Start a new remote desktop session on cortex and open the Terminal app.

## AIND ephys pipeline

First we'll run the [AIND ephys pipeline](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline) for spike sorting and quality metrics.
We use the pipeline code exactly as-is, from the AIND GitHub repo.

We use our own [cortex.config](./aind-ephys-pipeline/cortex.config) file to configure Nextflow for running on cortex.  This is where we specify the lab's storage directory `/vol/cortex/cd4/geffenlab/`.  This is also how we share resources with other cortex users -- instead of taking up all available resources.  In particular:
 - Use GPU at index 3, rather all GPUs or defaulting to GPU index 0.
 - Use 10 CPU cores at a time, instead of all of them.
 - Use up to 64GB of memory at a time, instead of unbounded memory.

To run the pipeline use our Python script [run_pipeline.py](./scripts/run_pipeline.py).  This script calls `nextflow run` to run the pipeline and also saves detailed logs along with other pipeline outputs.
We tell it which pipeline to run with the `--workflow` argument.  We specifiy the configuration with `--config`.  We also pass the `experimenter`, `--subject`, and `--date` for the session we want to process.

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --config geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config \
  --experimenter BH \
  --subject AS20-minimal3 \
  --date 03112025
```

The pipeline run should take only a few minutes.  A clean run should end with a summary like this:

```
Completed at: 14-Aug-2025 15:16:36
Duration    : 5m 17s
CPU hours   : 0.7
Succeeded   : 12
```

## AIND ephys pipeline (repeat)

Nextflow has the ability to reuse processing results from previous runs.  If it determines that the pipeline code and input data for a given step have not changed, it can skip execution of that step and reuse existing results.  To see this in action, use the `-resume` option.

For example, run the same pipeline again:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --config geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config \
  --experimenter BH \
  --subject AS20-minimal3 \
  --date 03112025 \
  -resume
```

We are calling Nextflow via our Python wrapper script [run_pipeline.py](./scripts/run_pipeline.py).  Extra command line arguments like `-resume` will be passed on to Nextflow iteslf.

This should take only a few seconds and end with a similar summary as before.  Nextflow should detect that nothing has changed and reuse all of the existing results.

## AIND ephys pipeline results

The pipeline will write results into a `processed_data/` subdirectory of the Geffen lab storage directory.

```
/vol/cortex/cd4/geffenlab/processed_data/
```

As with the `raw_data/` subdirectory, we organize `processed_data/` by experimenter initials, subject, date, and data type.

Here's a summary of the `raw_data/` and `processed_data/` subdirectories, after running the AIND ephys pipeline.

```
/vol/cortex/cd4/geffenlab/
├── raw_data/
│   └── BH/
│       └── AS20-minimal3/
│           └── 03112025/
│               ├── behavior/               # unchanged
│               └── ecephys/                # unchanged
└── processed_data/
    └── BH/
        └── AS20-minimal3/
            └── 03112025/
                └── sorted/                 # new
                    ├── nextflow/
                    ├── quality_control/
                    ├── nwb/
                    ├── preprocessed/
                    ├── spikesorted/
                    ├── curated/
                    ├── postprocessed/
                    └── visualization/
```

## Geffen lab ephys pipeline

Now we can run the [Geffen lab ephys pipeline](https://github.com/benjamin-heasly/geffenlab-ephys-pipeline) for combining data modalities and producing summary figures.

Again we use [run_pipeline.py](./scripts/run_pipeline.py).  This time we specify differnt `--workflow` and `--config`, but the same `--experimenter`, `--subject`, and `--date`.

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow geffenlab-ephys-pipeline/pipeline/main.nf \
  --config geffenlab-ephys-pipeline/pipeline/cortex.config \
  --experimenter BH \
  --subject AS20-minimal3 \
  --date 03112025
```

One of the pipeline steps will bring up a [Phy](https://phy.readthedocs.io/en/latest/) window within your remote desktop session, where you can do manual sorting curation.
Close the Phy window to allow the pipeline to continue.

In Phy you should mark several clusters as "good" so that downstream analysis will have clusters to work with.

This pipeline should finish in a few minutes (plus Phy curation time) and should end by printing a short summary.

## Geffen lab ephys pipeline results

As with the AIND pipeline, the Geffen lab pipeline writes results into the an `analysis/` subdirectory with files organized by subject, date, and data type.

Here's a summary of the data and analysis subdirectories, after running the Geffen lab pipeline:

```
/vol/cortex/cd4/geffenlab/
├── raw_data/
│   └── BH/
│       └── AS20-minimal3/
│           └── 03112025/
│               ├── behavior/               # unchanged
│               └── ecephys/                # unchanged
└── processed_data/
│   └── BH/
│       └── AS20-minimal3/
│           └── 03112025/
│               └── sorted/                 # unchanged
│               ├── curated/                # new
│               └── exported/               # new
└── analysis/                               # new
    └── BH/
        └── AS20-minimal3/
            └── 03112025/
                └── synthesis/
                    ├── AS20-minimal3-03112025.pkl
                    └── figures/
                        └── AS20-minimal3-03112025_neurons_1.png
```

The new `synthesis/` subdirectory contains a Python `.pkl` with dataframes from different modalities aligned in time, and summary figure(s) from the lab's [summary-plotting-scripts](./summary-plotting-scripts.md).

## Seeing pipeline results

You can see pipeline outputs from your remote desktop session.

 - Click `Activities` in the upper left.
 - Choose `Files` in the bottom meny that appears.
 - Click in the address bar at the top of the Files window and type or paste: `/vol/cortex/cd4/geffenlab`

You should see our subdirectories like `nextflow/`, `raw_data/`, `processed_data/`, and `analysis/`.  You can navigate within these to find pipeline results, for example navigate to `analysis/BH/AS20-minimal3/03112025/synthesis`.

## Downloading pipeline results

Please use the instructions in [cortex-moving-data.md](./cortex-moving-data.md) to download pipeline results from cortex to your local lab machine.

# Process a full `AS20` dataset

If all of the above worked then you should be ready to run the same pipelines again, this time on a full dataset.

Again, open a Terminal in a cortex remote desktop session.

Anjali uploaded a full dataset for subject `AS20` to the Geffenlab `raw_data/` subdirectory on cortex.
This dataset looks similar to the testing dataset above, but the files are bigger.

```
/vol/cortex/cd4/geffenlab/
└── raw_data/
    └── AS/
        └── AS20/
            └── 03112025/
                ├── behavior/
                │   ├── AS20_031125_trainingSingle6Tone2024_0_39.mat
                │   └── AS20_031125_trainingSingle6Tone2024_0_39.txt
                └── ecephys/
                    └── AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/
                        ├── AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.meta
                        ├── AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.bin
                        └── AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/
                            ├── AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.bin    
                            └── AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.meta
```

## AIND ephys pipeline

Running the AIND ephys pipeline on the full dataset looks almost exactly like running on the minimal testing dataset.

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --config geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config \
  --experimenter AS \
  --subject AS20 \
  --date 03112025
```

This time we specify the `--experimenter` as `AS` and the `--subject` as `AS20`.

Processing the full dataset will take longer than before, but it should still take less than an hour.  A clean run should end with a summary like this:

```
Completed at: 14-Aug-2025 15:58:23
Duration    : 27m 19s
CPU hours   : 3.8
Succeeded   : 12
```

## Geffen lab ephys pipeline

We can run the Geffen lab ephys pipeline in much the same way:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow geffenlab-ephys-pipeline/pipeline/main.nf \
  --config geffenlab-ephys-pipeline/pipeline/cortex.config \
  --experimenter AS \
  --subject AS20 \
  --date 03112025
```

Again, this should take a few minutes and end with a summary like this:

```
Completed at: 14-Aug-2025 16:26:19
Duration    : 4m 50s
CPU hours   : 1.3
Succeeded   : 5
```

