#! /bin/bash

set -e

ANALYSIS_ROOT=/home/ninjaben/codin/geffen-lab-data/analysis
SUBJECT=AS20-minimal
DATE=03112025
export ANALYSIS_PATH="$ANALYSIS_ROOT/$SUBJECT/$DATE/"
export RESULTS_PATH="$ANALYSIS_ROOT/$SUBJECT/$DATE/exported"
mkdir -p "$RESULTS_PATH"

./nextflow-25.04.6-dist -C geffenlab-export-pipeline/pipeline/main.config run geffenlab-export-pipeline/pipeline/main.nf
