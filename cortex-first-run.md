# Cortex First Run

This doc should help with your first pipeline run on cortex, using some known data.

Before running pipelines you'll need to do some one-time [cortex user setup](./cortex-user-setup.md) for your cortex user account.

The instructions below show how to process lab data using the [AIND ephys pipeline](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline) for spike sorting and quality metrics, and the [Geffen lab ephys pipeline](https://github.com/benjamin-heasly/geffenlab-ephys-pipeline) for combining data modalities and producing summary figures.


# Data locations


Before processing we need to put the data on cortex.  Geffen lab data have been assigned to a specific directory on cortex:

```
/vol/cortex/cd4/geffenlab/
```

Raw, original rig data should go into a `data/` subdirectory of this storage directory.

```
/vol/cortex/cd4/geffenlab/data/
```

Within this `data/` subdirectory we can orgaize files by subject, date, and data modality.

For example we have a minimal testing dataset that uses the following:
 - subject: `AS20-minimal2`
 - date: `03112025`
 - modalities: `behavior` and `ecephys`

Here's the minimal testing dataset at a glance:

```
/vol/cortex/cd4/geffenlab/
└── data/
    └── AS20-minimal2/
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

The subject id `AS20-minimal2` is unusual.  It means the original data are from subject `AS20`, but for testing we created a smaller version of the dataset (just a few trials) using tools in [geffenlab-minimal-data](https://github.com/benjamin-heasly/geffenlab-minimal-data).

# Process the `AS20-minimal2` dataset

Let's start by processing a small testing dataset for subject `AS20-minimal2`.  This processing run should only take a few minutes.

Log in to cortex and connect to a screen session.

```
ssh -Y ben@128.91.19.199

screen
# or
screen -x
```

Use your own cortex username rather than `ben`.

## AIND ephys pipeline

First we'll run the [AIND ephys pipeline](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline) for spike sorting and quality metrics.
We use the pipeline code exactly as-is, from the AIND GitHub repo.

We use our own [cortex.config](./aind-ephys-pipeline/cortex.config) file to configure Nextflow for running on cortex.  This is where we specify the lab's storage directory `/vol/cortex/cd4/geffenlab/`.  This is also how we share resources with other cortex users -- instead of taking up all available resources.  In particular:
 - Use GPU at index 3, rather all GPUs or defaulting to GPU index 0.
 - Use 10 CPU cores at a time, instead of all of them.
 - Use up to 64GB of memory at a time, instead of unbounded memory.

To run the pipeline we invoke Nextflow.  We tell it which pipeline to `run`, and to use our `cortex.config` configuration with `-C`.  We pass as parameters the `--subject` and `--date` of the dataset we want to process.

```
cd ~/nextflow
conda activate nextflow

NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config \
  run aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --subject AS20-minimal2 \
  --date 03112025
```

We need to set a Nextflow option, `NXF_DISABLE_PARAMS_TYPE_DETECTION=1`.  This allows us to use dates with a leading `0`.  Otherwise Nextflow would treat the date as a number, and discard the leading `0`.

The pipeline run should take only a few minutes.  A clean run should end with a summary like this:

```
Completed at: 14-Aug-2025 15:16:36
Duration    : 5m 17s
CPU hours   : 0.7
Succeeded   : 12
```

## AIND ephys pipeline (repeat)

Nextflow has the ability to reuse processing results from previous runs.  If it determines that the pipeline code and input data for a given step have not changed, it can skip execution of that step and reuse existing results.  To see this in action, use the `-resume` option when calling Nextflow.

For example, run the same pipeline again:

```
cd ~/nextflow
conda activate nextflow

NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config \
  run aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --subject AS20-minimal2 \
  --date 03112025 \
  -resume
```

This should take only a few seconds and end with a similar summary as before.  Nextflow should detect that nothing has changed and reuse all of the existing results.

## AIND ephys pipeline results

The pipeline will write results into an `analysis/` subdirectory of the Geffen lab storage directory.

```
/vol/cortex/cd4/geffenlab/analysis/
```

As with the `data/` subdirectory, we organize `analysis/` by subject, date, and data type.

Here's a summary of the `data/` and `analysis/` subdirectories, after running the AIND ephys pipeline.

```
/vol/cortex/cd4/geffenlab/
├── data/
│   └── AS20-minimal2/
│       └── 03112025/
│           ├── behavior/   # unchanged
│           └── ecephys/    # unchanged
└── analysis/
    └── AS20-minimal2/
        └── 03112025/
            └── sorted/     # new
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

Again we invoke Nextflow, telling it which pipeline to `run` and which config to use with `-C`.  We pass in the `--subject` and `--date`.

```
cd ~/nextflow
conda activate nextflow

NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/pipeline/cortex.config \
  run geffenlab-ephys-pipeline/pipeline/main.nf \
  --subject AS20-minimal2 \
  --date 03112025
```

Assuming you logged in to cortex using `ssh -Y` one of the pipeline steps will bring up a [Phy](https://phy.readthedocs.io/en/latest/) window on your local machine, where you can do manual sorting curation.  Close the Phy window to allow the pipeline to continue.

In Phy you should mark several clusters as "good" so that downstream analysis will have clusters to work with.

This pipeline should finish in a few minutes (plus Phy curation time) and should end by printing a short summary.

## Geffen lab ephys pipeline results

As with the AIND pipeline, the Geffen lab pipeline writes results into the an `analysis/` subdirectory with files organized by subject, date, and data type.

Here's a summary of the data and analysis subdirectories, after running the Geffen lab pipeline:

```
/vol/cortex/cd4/geffenlab/
├── data/
│   └── AS20-minimal2/
│       └── 03112025/
│           ├── behavior/   # unchanged
│           └── ecephys/    # unchanged
└── analysis/
    └── AS20-minimal2/
        └── 03112025/
            ├── sorted/     # unchanged
            ├── curated/    # new
            ├── exported/   # new
            └── synthesis/  # new
                ├── AS20-minimal2-03112025.pkl
                └── figures/
                    └── AS20-minimal2-03112025_neurons_1.png
```

The `synthesis/` subdirectory contains the results of the lab's [population-analysis](https://github.com/jcollina/population-analysis) code, including a Python `.pkl` with dataframes from different modalities aligned in time, and summary figure(s).

## Getting pipeline results

When the pipelines are finished, you can log out from cortex and copy pipeline results to your local machine.

Detach from screen and exit from cortex:

```
screen -d
exit
```

From WSL on your local machine create a directory to contain the results.  The following will create a folder on the Windows desktop called `ephys-pipeline-outputs`.  We can copy results here and organize them by subject and date.

```
mkdir -p /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/AS20-minimal2/03112025
```

In WSL change to this directory and copy results from cortex using `scp`.  "scp" stands for "secure copy."  It will prompt you for the same password you use with `ssh`:

```
cd /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/AS20-minimal2/03112025
scp -r ben@128.91.19.199:/vol/cortex/cd4/geffenlab/analysis/AS20-minimal2/03112025/synthesis .
```

As with `ssh` you'd use your own username rather than `ben`.

Now you should now be able to open `ephys-pipeline-outputs` on the Windows desktop and browse to the results.

# Process a full `AS20` dataset

If all of the above worked then you should be ready to run the same pipelines again, this time on a full dataset.

Log in to cortex and reconnect to your screen session.

```
ssh -Y ben@128.91.19.199
screen -x
```

Anjali uploaded a full dataset for subject `AS20` to the Geffenlab `data/` subdirectory on cortex.
This dataset looks similar to the testing dataset above, but the files are bigger.

```
/vol/cortex/cd4/geffenlab/
└── data/
    └── anjali/
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
cd ~/nextflow
conda activate nextflow

NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config \
  run aind-ephys-pipeline/pipeline/main_multi_backend.nf \
  --data_root /vol/cortex/cd4/geffenlab/data/anjali/ \
  --analysis_root /vol/cortex/cd4/geffenlab/analysis/anjali/ \
  --subject AS20 \
  --date 03112025
```

This time we specify the `--subject` as `AS20`.  We also specify the `--data_root` and `--analysis_root` explicitly since these have an extra path component for `anjali`.

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
cd ~/nextflow
conda activate nextflow

NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
  -C geffenlab-ephys-pipeline/pipeline/cortex.config \
  run geffenlab-ephys-pipeline/pipeline/main.nf \
  --data_root /vol/cortex/cd4/geffenlab/data/anjali/ \
  --analysis_root /vol/cortex/cd4/geffenlab/analysis/anjali/ \
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

## Getting pipeline results

Copying results for the full dataset is similar to copying results from the minimal test dataset.  Detach from screen and exit from cortex:

```
screen -d
exit
```

In WSL on your local machine create a directory to contain the results.

```
mkdir -p /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/AS20/03112025
```

Change to the `ephys-pipeline-outputs` directory and copy results from cortex using `scp`:

```
cd /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/AS20/03112025
scp -r ben@128.91.19.199:/vol/cortex/cd4/geffenlab/analysis/anjali/AS20/03112025/synthesis .
```

### Nextflow visualzations

It might also be interesting to see pipeline visualizations created by Nextflow.

Create a subfolder for these and `scp` them:

```
cd /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/AS20/03112025
mkdir sorted
scp -r ben@128.91.19.199:/vol/cortex/cd4/geffenlab/analysis/anjali/AS20/03112025/sorted/nextflow sorted/nextflow
scp -r ben@128.91.19.199:/vol/cortex/cd4/geffenlab/analysis/anjali/AS20/03112025/nextflow .
```

You should now be able to open `ephys-pipeline-outputs` on the Windows desktop and browse to the Nextflow visualizations.
Visualizations for the AIND ephys pipeline are in the `sorted/nextflow/` subfolder.  Visualizations for the Geffen lab ephys pipeline are in the `nextflow/` subfolder.

### AIND pipeline visualizations

The AIND ephys pipeline also produces some of its own visualizations related to spike sorting and quality control.  You might copy these as well:

```
cd /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/AS20/03112025
scp -r ben@128.91.19.199:/vol/cortex/cd4/geffenlab/analysis/anjali/AS20/03112025/sorted/visualization/ sorted/visualization/
```
