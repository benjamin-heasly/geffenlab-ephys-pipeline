#! /bin/bash

set -e

DATA_ROOT=/home/ninjaben/codin/geffen-lab-data/data
ANALYSIS_ROOT=/home/ninjaben/codin/geffen-lab-data/analysis

SUBJECT=AS20-minimal
DATE=03112025

export DATA_PATH="$DATA_ROOT/$SUBJECT/$DATE"
export ANALYSIS_PATH="$ANALYSIS_ROOT/$SUBJECT/$DATE"

./nextflow-25.04.6-dist -C geffenlab-export-pipeline/pipeline/main.config run geffenlab-export-pipeline/pipeline/main.nf
