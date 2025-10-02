# Session summary plotting scripts

This document describes how to configure session summary plotting scripts that run at the end of the Geffen lab ephys pipeline.

For each session, the pipeline produces a [Python pickel](https://docs.python.org/3/library/pickle.html) data file with a name like `summary.pkl`.
The pickel contains sorted clusters and spike times aligned with behavioral data.
It's small enough to download locally and do analysis with, for example using notebook code from the lab's [population-analysis](https://github.com/jcollina/population-analysis) repo.

In addition, the pipeline will use the same `summary.pkl` to generate summary plots for each session.
You can configure which plots are generated and add new ones when you need to.

## Choose which plots are generated

Choosing which plots are generated is part of the Nextflow configuration for a pipeline run, as described in [pipeline-configurations](./pipeline-configurations.md).

You can set the value of `synthesis_plotting_scripts` to be a list of script names, separated by spaces.  For example:

```
synthesis_plotting_scripts = "complex_condition demo"
```

This would produce two plots, the `complex_condition` plot and the `demo` plot.

## What plots can you choose from?

The plots you can choose from are defined as part of the synthesis step (which runs at the end of the pipeline).
The code for the synthesis step is in the [geffenlab-synthesis](https://github.com/benjamin-heasly/geffenlab-synthesis) repo.

The plotting scripts themselves are in the [`code/plotting_scripts`](https://github.com/benjamin-heasly/geffenlab-synthesis/tree/main/code/plotting_scripts) subdirectory of the synthesis repo.
In there you will see scripts like [`complex_condition.py`](https://github.com/benjamin-heasly/geffenlab-synthesis/blob/main/code/plotting_scripts/complex_condition.py) and [`demo.py`](https://github.com/benjamin-heasly/geffenlab-synthesis/blob/main/code/plotting_scripts/demo.py).  The names of these scripts are the names of the `synthesis_plotting_scripts` that you can choose from (minus the `.py` at the end).

## How do plotting scripts work?

Comments in [`demo.py`](https://github.com/benjamin-heasly/geffenlab-synthesis/blob/main/code/plotting_scripts/demo.py) describe how the script itself works and how it fits into the overall pipeline run.  In short:

 - Plotting scripts should expect to find a `summary.pkl` in the current directory.
 - They should have a `plot()` function that works with no arguments.
 - They should write figures into a `figures/` subdirectory of the current directory.

Within these conventions, each plotting script can run arbitrary code and generate arbitrary plots.

## How do you add a new plotting script?

To add a new plotting script, make a copy of an existing script, like [`demo.py`](https://github.com/benjamin-heasly/geffenlab-synthesis/blob/main/code/plotting_scripts/demo.py), and modify the `plot()` function.

Save your new script in the same [`code/plotting_scripts`](https://github.com/benjamin-heasly/geffenlab-synthesis/tree/main/code/plotting_scripts) subdirectory of the [geffenlab-synthesis](https://github.com/benjamin-heasly/geffenlab-synthesis) repo.  Commit your changes with `git commit` and `git push` your changes to GitHub.  This puts your script where it belongs, and where the `synthesis` step can find it by name.

## Releasing a new plotting script

There are a few more steps before you can do a full pipeine run with your new script!

These might seem extra, but they have motivation.  Using an explicit relase process based on Docker images allows us to distribute our code along with its dependencies, and run it in a reproducible way across different environments or different times.  Old versions will still exist, and will still work they way they did, even as time goes on.

### New repo tag and Docker image build

First, you must create a new git tag for the [geffenlab-synthesis](https://github.com/benjamin-heasly/geffenlab-synthesis) repo.  This will cause a [synthesis step Docker image](https://github.com/benjamin-heasly/geffenlab-synthesis/pkgs/container/geffenlab-synthesis) to be built and published on GitHub.  See more details for this in the `geffenlab-synthesis` [README](https://github.com/benjamin-heasly/geffenlab-synthesis/pkgs/container/geffenlab-synthesis#building-docker-image-versions).


### Update Docker image version in the pipeline

Second, you must update the Geffen lab ephys pipeline here in this repo to use your new Docker image version.
The Docker image version is specified in the pipeline code at or near [main.nf, line 126](https://github.com/benjamin-heasly/geffenlab-ephys-pipeline/blob/master/pipeline/main.nf#L126).

The code there looks similar to this:

```
process geffenlab_synthesis {
    tag 'geffenlab_synthesis'
    container 'ghcr.io/benjamin-heasly/geffenlab-synthesis:v0.0.11'

    ...
}
```

This says that the `synthesis` step uses the Docker `container` image called `ghcr.io/benjamin-heasly/geffenlab-synthesis:v0.0.11`.  That's a mouthful, but the version we need to change is just the last part: `v0.0.11`.

To update the pipeline from version `v0.0.11` to `v0.0.12`, you would just change that last number:

```
process geffenlab_synthesis {
    tag 'geffenlab_synthesis'
    container 'ghcr.io/benjamin-heasly/geffenlab-synthesis:v0.0.12'

    ...
}
```

Then commit your change to `main.nf` and push your change to GitHub.

### Get the pipeline update on cortex

Finally, you must update the pipeline conde where you're runnign it.
On cortex this means pulling the latest changes for this pipeline repo:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline
git pull
```

## How do you test a new script?

You can test your plotting script locally while you're still working on it.

You'll need a `summary.pkl` to work with, like one [downloaded from a previous pipeline run](https://github.com/benjamin-heasly/geffenlab-ephys-pipeline/blob/master/cortex-moving-data.md#download-results-from-cortex).

If you run your new script from the same directory that contais `summary.pkl`, it should find the data and generate whatever plots that you code up.

You'll probably need some Python dependencies in place, like matplotlib or numpy.
You could install these locally via `pip install`.

Better still, you could set up the same conda environment that the pipeline uses when it runs.
This environment is defined in the [geffenlab-synthesis](https://github.com/benjamin-heasly/geffenlab-synthesis) repo.

To set up this conda environment locally:

```
git clone --recurse-submodules https://github.com/benjamin-heasly/geffenlab-synthesis.git
cd geffenlab-synthesis/environment
conda env create -f environment.yml
conda activate synthesis
```

This will clone the synthesis repo, along with the population-analysis repo as a git submodule.
You'll need permission to access [population-analysis](https://github.com/jcollina/population-analysis) from GitHub.

Now you can run your plotting script using the same Python environment that the pipelines use.
Change directory to where you downloaded `summary.pkl`, and run your plotting script from there.

```
conda activate synthesis
cd where/you/downloded/the/pickel
python where/you/cloned/geffenlab-synthesis/code/plotting_scripts/your_new_script.py
```

This should allow you to iterate quickly to plot what you want, before going through the whole release process above.
