# geffenlab-ephys-pipeline

This repo contains [Nextflow](https://www.nextflow.io/) pipelines and Python scripts for processing Geffen lab ephys data.

For each datset:
 - First we want to run the [aind-ephys-pipeline](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline).  This will do spike sorting and automated curation based on quality metrics.
 - Then we can run the Geffen lab's [phy-export](./phy-export/phy-export.nf) pipeline.  This will convert the `aind-ephys-pipeline` results to the format expected by Phy, for manual curation.

From there we'll have a few options for manual curation and further processing (work in progress...).

# Getting started on cortex

First, you should go through our [cortex-user-setup.md](./docs/cortex-user-setup.md) docs, to get your local and cortex environments set up.

# Running pipelines

Here are docs for several steps that should be working so far:
 - Upload session data to cortex: [cortex-upload-data.md](./docs/cortex-upload-data.md)
 - Run the AIND sorting pipeline: [run-aind-ephys-pipeline.md](./docs/run-aind-ephys-pipeline.md)
 - Run the phy-export pipeline: [run-phy-export.md](./docs/run-phy-export.md)

The steps above will save sorting results in Phy format, on cortex.
From there we have some options.

You can do Phy curation on cortex, via remote desktop.  This should work, but might be slow (for now):
 - Phy curation on cortex: [phy-on-cortex-remote-desktop](./docs/run-phy.md#phy-on-cortex-remote-desktop)

When you're done with Phy on cortex (or if you skip that step) you can download results from cortex:
 - Download results from cortex: [cortex-download-results.md](./docs/cortex-download-results.md)

You can also to the Phy curation locally, using the results you downloaded:
 - Local Phy curation: [phy-local-with-data-download](./docs/run-phy.md#phy-local-with-data-download)

When you're done with local Phy curation, you can upload the curated data back to cortex:
 - Upload analysys back to cortex: [upload-analysis.md](./docs/upload-analysis.md)

# Pipeline steps and Docker images 

All of the steps in the Geffen lab ephys pipeline are all based on [Docker images](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/).  Each image contains custom Python code, bundled into a reproducible environment along with the Python runtime and other dependencies.

Each of our Docker images lives in its own repostory, described below.

## geffenlab-ecephys-phy-export

The [geffenlab-ecephys-phy-export](https://github.com/benjamin-heasly/geffenlab-ecephys-phy-export) image has code to convert AIND ephys pipeline results to the Phy format, using [SpikeInterface](https://spikeinterface.readthedocs.io/en/stable/).

It also creates a default `cluster_info.tsv`, which makes it optional to do manual curation via Phy.

## geffenlab-spikeglx-tools

The [geffenlab-spikeglx-tools](https://github.com/benjamin-heasly/geffenlab-spikeglx-tools) image has tools for processing SpikeGLX outputs, like [CatGT](https://billkarsh.github.io/SpikeGLX/#catgt) and [TPrime](https://billkarsh.github.io/SpikeGLX/#tprime).

It has Python wrappers for calling these tools in a more familiar Python style.

## geffenlab-phy-desktop

The [geffenlab-phy-desktop](https://github.com/benjamin-heasly/geffenlab-phy-desktop) image has a [Phy](https://phy.readthedocs.io/en/latest/) installation that we can use for interactive curation.

## geffenlab-synthesis

The [geffenlab-synthesis](https://github.com/benjamin-heasly/geffenlab-synthesis) image incorporates the lab's [population-analysis](https://github.com/jcollina/population-analysis) code for aligning and combining data into dataframes, and plotting session summary figures.
