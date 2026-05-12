# geffenlab-ephys-pipeline

This repository contains [Proceed](https://benjamin-heasly.github.io/proceed/) [pipelines](./proceed/) and Python [scripts](./scripts/) for processing Geffen lab ephys data.

This repository goes with several other repositories that define inividual processing steps and Docker images:
 - [geffenlab-spikeglx-tools](https://github.com/benjamin-heasly/geffenlab-spikeglx-tools): CatGT, TPrime, Python scripts
 - [geffenlab-kilosort4](https://github.com/benjamin-heasly/geffenlab-kilosort4): Kilosort4, NVIDIA and CUDA dependencies, ProbeInterface
 - [geffenlab-bombcell](https://github.com/benjamin-heasly/geffenlab-bombcell): Bombcell
 - [geffenlab-phy-desktop](https://github.com/benjamin-heasly/geffenlab-phy-desktop): interactive Phy environment
 - [geffenlab-data-summary](https://github.com/benjamin-heasly/geffenlab-data-summary): population analysis data summary and plots
 - [geffenlab-minimal-data](https://github.com/benjamin-heasly/geffenlab-minimal-data): utilities for preparing small test datasets

# Getting started

To set up your local and cortex environment for running pipelines, see [cortex-user-setup.md](./docs/cortex-user-setup.md).

# Running pipelines

Here's the general, intended workflow along with relevant [docs/](./docs/).

## Intended workflow

### upload data to cortex
Behavioral and neural data would be created on a rig machine.  See [upload-data.md](./docs/upload-data.md) to locate data for each session and upload to cortex using standardized directory structure and file permissions.

### run a pipeline on cortex
On cortex process data for each session using the `proceed` command and a [pipeline YAML file](./proceed/).  See [pipeline-test-run.md](./docs/pipeline-test-run.md) and [setup-poc.md](./proceed/setup-poc.md).  WIP -- these should be combined.

### configure Kilosort4 and Bombcell with JSON
Both Kilosort4 and Bombcell accept dozens of configuration options / parameters that guide their behavior.  You can specify these per probe, with JSON files.  If you locate the JSON files near the raw data and name them according to a convention, then the pipeline will automatically apply these to the relevent steps.  See [pipeline-config.md](./docs/pipeline-config.md).

### run Phy on cortex
The pipieline will run Kilosort 4 and Bombcell.  You can view and revise the results with Phy, see [run-phy.md](./docs/run-phy.md).

### re-run pipeline steps on cortex
You might need to re-run one or more pipeline steps, for example after manual curation.  See [reprocessing.md](./docs/reprocessing.md).  WIP -- this doesn't exist yet.

### download `analysis` results locally
Pipelines deal with large files of raw data and intermediate processing results.  They should produce relatively small results in an `analysis` subdirectory.  See [download-results.md](./docs/download-results.md) to download the `analysis` subdirectory for a session.

### archive data from cortex
If you decide to archive a dataset, you can copy the raw behavioral and neural data to Amazon S3.  You can optionally delete these from cortex as well.  See [archive-data.md](./docs/archive-data.md).

# Docker images

Our pipeline steps are based on [Docker images](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/).  Each image contains custom Python code along with the Python runtime and other dependencies, bundled into a portable, reproducible environment.

The repositories mentioned at the top of this page are responsible for defining and producing these Docker images.  See the readme for each repository for details like where to find the Docker images on Github, and how to create new versions.

When running pipelines we download relevant Docker images and run commands within Docker containers.  Some Docker images are large, multiple GB.  See [docker-images.md](./docs/docker-images.md) for tips on how to manage Docker images and disk usage.
