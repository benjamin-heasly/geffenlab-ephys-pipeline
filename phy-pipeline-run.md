# Running the Phy pipeline

This doc should help you run the Phy pipeline for manual creation.
This pipeline is defined in [phy-pipeline/main.nf](./phy-pipeline/main.nf).

Before running this and other pipelines you'll need to do some one-time [cortex user setup](./cortex-user-setup.md) for your cortex user account and local lab machine.

The Phy pipeline is intended to run after the [AIND ephys pipeline](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline), which does spike sorting and generates quality metrics.
The Phy pipeline gives you a chance to do manual curation of sorted clusters.

# WIP...

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

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py \
  --workflow geffenlab-ephys-pipeline/phy-pipeline/main.nf \
  --config geffenlab-ephys-pipeline/phy-pipeline/cortex.config \
  --experimenter BH \
  --subject AS20-minimal3 \
  --date 03112025
```
