# Initial setup with Proceed

This doc should help us clean up from a previous Nextflow environment and set up a new Proceed environment, on cortex.

# Prerequisites

To work with Proceed we'll need Python and Docker installed.
In addition, for Kilosort 4 we'll need NVIDIA and CUDA drivers installed, and the nvidia container toolkit.

These are already installed on cortex.
Potentially these could also be installed locally.

We'll need Conda to manage our Python environment.

# Docker images

We can get rid of several older Docker images and images from the AIND Nextflow pipeline.

List the currently installed Docker images.

```
docker images
```

We want these images:
```
IMAGE                                                      ID             DISK USAGE   CONTENT SIZE
ghcr.io/benjamin-heasly/geffenlab-bombcell:v0.0.6          9f3b4dc71b37       3.08GB             0B
ghcr.io/benjamin-heasly/geffenlab-kilosort4:v0.0.3         9a37f2e60c08       10.9GB             0B
ghcr.io/benjamin-heasly/geffenlab-phy-desktop:v0.0.5       7c679a9d42d6       5.14GB             0B
ghcr.io/benjamin-heasly/geffenlab-spikeglx-tools:v0.0.17   f6060f4cd4c9       2.69GB             0B
```

If there are other images in there, we can remove them by `ID`.

```
docker rmi 9f3b4dc71b37
```

If there are images missing we can `docker pull` them.
The pipeline would automatically pull them as needed.
Pulling them explicitly lets us see the progress.

```
docker pull ghcr.io/benjamin-heasly/geffenlab-bombcell:v0.0.6
docker pull ghcr.io/benjamin-heasly/geffenlab-kilosort4:v0.0.3
docker pull ghcr.io/benjamin-heasly/geffenlab-phy-desktop:v0.0.5
docker pull ghcr.io/benjamin-heasly/geffenlab-spikeglx-tools:v0.0.17
```

# This repo

We'll need this repo.
We should be able to work in our home dirs.

```
cd ~
git clone https://github.com/benjamin-heasly/geffenlab-ephys-pipeline.git
```

# Conda environment

We can use Conda to install our `geffen-pipelines` Conda environment.

```
# Remove any old Nextflow environment.
conda env remove -n geffen-pipelines

cd ~/geffenlab-ephys-pipeline
conda env create -f geffen-pipelines.yml
```

# Verify proceed

Proceed should now be installed.

```
conda activate geffen-pipelines
proceed --help
```

# Run a pipeline with small data

Test one of our pipelines with a small dataset.

```
conda activate geffen-pipelines
cd ~/geffenlab-ephys-pipeline

proceed run proceed/as-nidq.yaml --args experimenter=BH subject=AS20-minimal3 date="03112025"
```

This should take several minutes, but not an hour, to complete.

# View the results in Phy

We can view the sorting results witih Phy, directly on Cortex.
Running this way, Phy might be annoyingly slow to respond.
But it should run, and that tells us a lot.

```
conda activate geffen-pipelines
cd ~/geffenlab-ephys-pipeline/scripts

python run_phy.py --experimenter BH --subject AS20-minimal3 --date "03112025"
```

# Process full-sized sessions

We can use the same pipeline to process a full session for AS.

```
conda activate geffen-pipelines
cd ~/geffenlab-ephys-pipeline

# single-probe NIDQ session
proceed run proceed/as-nidq.yaml --args experimenter=AS subject=AS20 date="03112025"

# dual-probe NIDQ session
proceed run proceed/as-nidq.yaml --args experimenter=AS subject=AS40 date="01062026"

# Look at results in Phy
cd ~/geffenlab-ephys-pipeline/scripts
python run_phy.py --experimenter AS --subject AS20 --date "03112025"
python run_phy.py --experimenter AS --subject AS20 --AS40 "01062026"
```

We can use a similar but different pipeline YAML to process OneBox-and-treadmill sessions for AD.

```
conda activate geffen-pipelines
cd ~/geffenlab-ephys-pipeline

# longer sessions with onebox and treadmill continuous signal
proceed run proceed/ad-onebox.yaml --args experimenter=AD subject=AD025 date="03102026"
proceed run proceed/ad-onebox.yaml --args experimenter=AD subject=AD025 date="03112026"

# Look at results in Phy
cd ~/geffenlab-ephys-pipeline/scripts
python run_phy.py --experimenter AD --subject AD025 --date "03102026"
python run_phy.py --experimenter AD --subject AD025 --AS40 "03112026"
```
