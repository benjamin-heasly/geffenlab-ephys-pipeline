# Download Results

This doc should help you download pipelines results from cortex to your local machine.

First, you'll need to do the one-time [cortex user setup](./cortex-user-setup.md) for your cortex user account and local lab machine.

# Download results from cortex

This repo has a Python script [download_results.py](../scripts/download_results.py) that should help downloading pipeline results from cortex to your local machine.  Internally this uses `ssh` to connect to cortex using your own user credentials.

Run this script from the WSL environment of your local lab machine:

```
# Go to the directory that will contain your pipeline-results/ folder.
# For example:
cd /mnt/c/Users/labuser/Desktop
conda activate geffen-pipelines

# Run our results download Python script.
python ~/geffenlab-ephys-pipeline/scripts/download_results.py
```

This will prompt you for the experimenter initials, subject id, and session date you want to download.  It will also ask for your cortex credentials.  For example:

```
2025-11-24 14:49:13,579 [INFO] Downloading files to local root: /mnt/c/Users/labuser/Desktop/pipeline-results
2025-11-24 14:49:13,579 [INFO] Downloading files from remote host: 128.91.19.199
2025-11-24 14:49:13,579 [INFO] Downloading files from remote processed data root: /vol/cortex/cd4/geffenlab/processed_data
2025-11-24 14:49:13,579 [INFO] Downloading files from remote analysis root: /vol/cortex/cd4/geffenlab/analysis
2025-11-24 14:49:13,579 [INFO] Downloading processed_data subdirs: ['logs', 'sorted/visualization']
Experimenter initials: BH
2025-11-24 14:49:15,727 [INFO] Downloading files for experimenter: BH
Subject ID: AS20-minimal3
2025-11-24 14:49:19,619 [INFO] Downloading files for subject id: AS20-minimal3
Session date MMDDYYYY: 03112025
2025-11-24 14:49:22,679 [INFO] Downloading files for session date: 03112025 (2025-03-11)
Remote username: ben
2025-11-24 14:49:24,531 [INFO] Downloading files as remote user: ben
Password for remote user ben:
2025-11-24 14:49:30,265 [INFO] Connecting to remote host: 128.91.19.199.
2025-11-24 14:49:40,067 [INFO] Connected (version 2.0, client OpenSSH_8.9p1)
2025-11-24 14:49:40,182 [INFO] Authentication (password) successful!
```

It will summarize what it finds in the session's `analysis/` subdirectory on cortex, and download all of these files:

```
2025-11-24 14:49:40,183 [INFO] Checking for remote analysis session directory /vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025:
phy-export
run_phy_20251124T184018UTC.log
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/params.py
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_exp_decay.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_spread.tsv
... etc ...
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/run_phy_20251124T184018UTC.log
2025-11-24 14:49:41,962 [INFO] Downloading files to: /mnt/c/Users/labuser/Desktop/pipeline-results
2025-11-24 14:49:42,026 [INFO] [chan 2] Opened sftp connection (server version 3)
```

It will also check selected subdirs of the session's `processed_data/` subdir, and summarize and download what if finds there:

```
2025-11-24 14:49:51,249 [INFO] Checking for remote processed data session directory /vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025:
logs
phy-export
sorted

2025-11-24 14:49:51,274 [INFO] Checking for processed data subdir logs:
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/phy-export_20251124T174934UTC_run_pipeline.log
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/aind-ephys-pipeline/nextflow-dag.html
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/aind-ephys-pipeline/nextflow-trace.txt
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/aind-ephys-pipeline/nextflow-timeline.html
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/aind-ephys-pipeline/nextflow-report.html
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/phy-export_20251124T175308UTC_process_detail.md
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/phy-export_20251124T174934UTC_nextflow.log
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/phy-export_20251124T175308UTC_nextflow.log
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/main_multi_backend_20251124T172227UTC_nextflow.log
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/main_multi_backend_20251124T172227UTC_run_pipeline.log
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/main_multi_backend_20251124T172227UTC_process_detail.md
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/phy-export_20251124T175308UTC_run_pipeline.log
2025-11-24 14:49:51,324 [INFO] Downloading files to: /mnt/c/Users/labuser/Desktop/pipeline-results

2025-11-24 14:49:51,958 [INFO] Checking for processed data subdir sorted/visualization:
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/sorted/visualization/block0_imec0.ap_recording1/traces_proc_seg0.png
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/sorted/visualization/block0_imec0.ap_recording1/motion.png
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/sorted/visualization/block0_imec0.ap_recording1/traces_full_seg0.png
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/sorted/visualization/block0_imec0.ap_recording1/drift_map.png
2025-11-24 14:49:52,004 [INFO] Downloading files to: /mnt/c/Users/labuser/Desktop/pipeline-results
2025-11-24 14:49:52,694 [INFO] [chan 2] sftp session closed.
2025-11-24 14:49:52,694 [INFO] OK.
```

When finished you should be able to browse your local `pipeline-results/` folder and see all the results.
For example, here's a `params.py` for Phy.

![Windows desktop files view](./download-results.png)


## Options

The example above used several default options like the cortex host address, the local directory to receive results, and which subfolders to download for the given session.
All of these can be modified from the command line as needed.  For details please see:

```
python geffenlab-ephys-pipeline/scripts/download_results.py --help
```
