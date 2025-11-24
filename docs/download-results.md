# Cortex Moving Data

This doc should help you download pipelines results from cortex to your local machine.

First, you'll need to do the one-time [cortex user setup](./cortex-user-setup.md) for your cortex user account and local lab machine.

# Download results from cortex

This repo has a Python script [download_results.py](./scripts/download_results.py) that should help downloading pipeline results from cortex to your local machine.  Internally this uses `ssh` to connect to cortex using your own user credentials.

Run this script from the WSL environment of your local lab machine:

```
# Go to the directory that will contain your `pipeline-results/`. folder of results.
# This is one example:
cd /mnt/c/Users/labuser/Desktop

# Run our results download Python script.
conda activate geffen-pipelines
python ~/geffenlab-ephys-pipeline/scripts/download_results.py
```

This will prompt you for the experimenter initials, subject id, and session date you want to download.  It will also ask for your cortex credentials.  For example:

```
2025-10-03 15:32:25,755 [INFO] Downloading files to local root: /mnt/c/Users/labuser/Desktop/pipeline-results
2025-10-03 15:32:25,755 [INFO] Downloading files from remote host: 128.91.19.199
2025-10-03 15:32:25,755 [INFO] Downloading files from remote processed data root: /vol/cortex/cd4/geffenlab/processed_data
2025-10-03 15:32:25,755 [INFO] Downloading files from remote analysis root: /vol/cortex/cd4/geffenlab/analysis
2025-10-03 15:32:25,755 [INFO] Downloading processing logs that match patterns: ['*.log', '*.md']
2025-10-03 15:32:25,755 [INFO] Downloading processed data subdirs: ['nextflow', 'sorted/nextflow', 'sorted/visualization']
Experimenter initials: BH
2025-10-03 15:32:29,387 [INFO] Downloading files for experimenter: BH

Subject ID: AS20-minimal3
2025-10-03 15:32:33,406 [INFO] Downloading files for subject id: AS20-minimal3

Session date MMDDYYYY: 03112025
2025-10-03 15:32:37,427 [INFO] Downloading files for session date: 03112025 (2025-03-11)

Remote username: ben
2025-10-03 15:32:38,939 [INFO] Downloading files as remote user: ben

Password for remote user ben:
```

It will summarize what it finds in the session's analysis subdirectory on cortex, and download all of these files:

```
2025-10-03 15:32:52,850 [INFO] Checking for remote analysis session directory /vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025:
synthesis
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/synthesis/figures/AS20-minimal3-03112025_demo.png
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/synthesis/figures/AS20-minimal3-03112025_neurons_1.png
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/synthesis/BH_AS20-minimal3_03112025_summary.pkl

2025-10-03 15:32:53,120 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/synthesis/figures/AS20-minimal3-03112025_demo.png
2025-10-03 15:32:53,158 [INFO] [chan 2] Opened sftp connection (server version 3)
2025-10-03 15:32:53,263 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/synthesis/figures/AS20-minimal3-03112025_neurons_1.png
2025-10-03 15:32:53,333 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/synthesis/BH_AS20-minimal3_03112025_summary.pkl
```

It will summarize what it finds in the sessions's processed data subdirectory on cortex:

```
2025-10-03 15:32:53,430 [INFO] Checking for remote processed data session directory /vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025:
curated
exported
main_20251003T190321UTC_nextflow.log
main_20251003T190321UTC_process_detail.md
main_20251003T190321UTC_run_pipeline.log
main_multi_backend_20251003T175141UTC_nextflow.log
main_multi_backend_20251003T175141UTC_process_detail.md
main_multi_backend_20251003T175141UTC_run_pipeline.log
nextflow
sorted
```

It will download log files from the session's processed data directory:

```
Found session processing logs: ['main_20251003T190321UTC_nextflow.log', 'main_20251003T190321UTC_run_pipeline.log', 'main_20251003T190321UTC_process_detail.md', 'main_multi_backend_20251003T175141UTC_nextflow.log', 'main_multi_backend_20251003T175141UTC_run_pipeline.log', 'main_multi_backend_20251003T175141UTC_process_detail.md']
2025-10-03 15:32:53,869 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/main_20251003T190321UTC_nextflow.log
2025-10-03 15:32:53,890 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/main_20251003T190321UTC_run_pipeline.log
2025-10-03 15:32:54,235 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/main_20251003T190321UTC_process_detail.md
2025-10-03 15:32:53,999 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/main_multi_backend_20251003T175141UTC_nextflow.log
2025-10-03 15:32:54,021 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/main_multi_backend_20251003T175141UTC_run_pipeline.log
2025-10-03 15:32:54,276 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/main_multi_backend_20251003T175141UTC_process_detail.md
```

When finished you should be able to open `pipeline-results` on the Windows desktop and browse to the results.

## Options

The example above used several default options like the cortex host address, the local directory to receive results, and which subfolders to download for the given session.
All of these can be modified from the command line as needed.  For details please see:

```
python geffenlab-ephys-pipeline/scripts/download_results.py --help
```
