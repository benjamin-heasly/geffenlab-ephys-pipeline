# Cortex Moving Data

This doc should help you upload data from a local lab machine to cortex, and download pipeline results from cortex to a local lab machine.

First, you'll need to do some one-time [cortex user setup](./cortex-user-setup.md) for your cortex user account and local lab machine.

# Upload data to cortex

This repo has a Python script [upload_data.py](./scripts/upload_data.py) that should help uploading data from your local lab machine to cortex.  Internally this uses `ssh` to connect to cortex, and the Python wrapper should add convenience.

Run this script from the WSL environment of your local lab machine:

```
cd ~
conda activate geffen-pipelines

python geffenlab-ephys-pipeline/scripts/upload_data.py
```

This will prompt you for the experimenter initials, subject id, and session date that you want to upload, plus an optional qualifier to further narrow down which files are uploaded.  It will also ask for your cortex credentials.  For example:

```
2025-10-03 12:53:51,379 [INFO] Uploading behavior files from : /mnt/c/Users/labuser/Desktop/Data
2025-10-03 12:53:51,379 [INFO] Using behavior .txt pattern: <SUBJECT>/**/*_<MM><DD><YY>_*.txt
2025-10-03 12:53:51,379 [INFO] Using behavior .mat pattern: <SUBJECT>/**/*_<MM><DD><YY>_*.mat
2025-10-03 12:53:51,379 [INFO] Uploading ephys files from : /mnt/c/Users/labuser/Desktop/Data
2025-10-03 12:53:51,379 [INFO] Using SpikeGLX .meta pattern: <SUBJECT>/**/*_<MM><DD><YYYY>_*.meta
2025-10-03 12:53:51,379 [INFO] Using Open Ephys .oebin pattern: <SUBJECT>/**/<YYYY>-<MM>-<DD>_*/*/*/*/structure.oebin
2025-10-03 12:53:51,379 [INFO] Uploading files to remote host: 128.91.19.199
2025-10-03 12:53:51,379 [INFO] Uploading files to remote raw data root: /vol/cortex/cd4/geffenlab/raw_data

Experimenter initials: BH
2025-10-03 12:53:54,300 [INFO] Uploading files for experimenter: BH

Subject ID: AS20-minimal2
2025-10-03 12:53:58,995 [INFO] Uploading files for subject id: AS20-minimal2

Session date MMDDYYYY: 03112025
2025-10-03 12:54:01,984 [INFO] Uploading files for session date: 03112025 (2025-03-11)

Qualifier like 'training','ap.bin', 'recording1', etc.  Leave blank to upload all:
2025-10-03 12:54:03,273 [INFO] Uploading all files.

Remote username: ben
2025-10-03 12:54:04,608 [INFO] Uploading files as remote user: ben

Password for remote user ben:
```

Based on the subject id, session date, and optional qualifier, the script will search local directories for behavior and ecephys files.  It will use [glob](https://docs.python.org/3/library/glob.html) patterns to select specific files of interest.

```
2025-10-03 12:54:11,149 [INFO] Searching local behavior_root for .txt like: AS20-minimal2/**/*_031125_*.txt
2025-10-03 12:54:11,201 [INFO]   AS20-minimal2/AS20-minimal2/03112025/behavior/AS20_031125_trainingSingle6Tone2024_0_39.txt
2025-10-03 12:54:11,225 [INFO] Searching local behavior_root for .mat like: AS20-minimal2/**/*_031125_*.mat
2025-10-03 12:54:11,240 [INFO]   AS20-minimal2/AS20-minimal2/03112025/behavior/AS20_031125_trainingSingle6Tone2024_0_39.mat
2025-10-03 12:54:11,262 [INFO] Searching local ephys_root for .meta like: AS20-minimal2/**/*_03112025_*.meta
2025-10-03 12:54:11,299 [INFO] Found .meta matches: [PosixPath('/mnt/c/Users/labuser/Desktop/Data/AS20-minimal2/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.meta'), PosixPath('/mnt/c/Users/labuser/Desktop/Data/AS20-minimal2/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.meta')]
2025-10-03 12:54:11,299 [INFO] Found spikeglx run dir: /mnt/c/Users/labuser/Desktop/Data/AS20-minimal2/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0
2025-10-03 12:54:11,306 [INFO]   AS20-minimal2/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.bin
2025-10-03 12:54:11,307 [INFO]   AS20-minimal2/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.meta
2025-10-03 12:54:11,307 [INFO]   AS20-minimal2/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.bin
2025-10-03 12:54:11,307 [INFO]   AS20-minimal2/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.meta
2025-10-03 12:54:11,307 [INFO] Searching local ephys_root for .oebin like: AS20-minimal2/**/2025-03-11_*/*/*/*/structure.oebin
2025-10-03 12:54:11,343 [INFO] Found .oebin matches: []
```

From all the files found, the script can use the optional qualifier to further restrict which files will be uploaded.  When the qualifier is provided, only files that contain the qualifier in their name will be uploaded.  For example, the qualifier "training" could be used to select "training" files but ignore "testing" files.

Before uploading, the script will show which files it plans to create on cortex and prompt for your confirmation.

```
2025-10-03 12:54:11,344 [INFO] Planning to create 6 files in remote data_root:
2025-10-03 12:54:11,344 [INFO]   BH/AS20-minimal2/03112025/behavior/AS20_031125_trainingSingle6Tone2024_0_39.txt
2025-10-03 12:54:11,344 [INFO]   BH/AS20-minimal2/03112025/behavior/AS20_031125_trainingSingle6Tone2024_0_39.mat
2025-10-03 12:54:11,344 [INFO]   BH/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.bin
2025-10-03 12:54:11,344 [INFO]   BH/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.meta
2025-10-03 12:54:11,344 [INFO]   BH/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.bin
2025-10-03 12:54:11,344 [INFO]   BH/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.meta
Do you want to upload these files?  Type 'yes' to proceed: yes
```

You must type `yes` to proceed.  Otherwise the script will exit before uploading.
If you do type `yes` the script will upload each file to cortex:

```
2025-10-03 12:54:14,411 [WARNING] Proceeding to upload files.
2025-10-03 12:54:14,411 [INFO] Connecting to remote host: 128.91.19.199.
2025-10-03 12:54:24,295 [INFO] Connected (version 2.0, client OpenSSH_8.9p1)
2025-10-03 12:54:24,416 [INFO] Authentication (password) successful!
2025-10-03 12:54:24,416 [INFO] Uploading to /vol/cortex/cd4/geffenlab/raw_data:
2025-10-03 12:54:24,416 [INFO]   BH/AS20-minimal2/03112025/behavior/AS20_031125_trainingSingle6Tone2024_0_39.txt
2025-10-03 12:54:24,764 [INFO] [chan 1] Opened sftp connection (server version 3)
2025-10-03 12:54:24,821 [INFO]   BH/AS20-minimal2/03112025/behavior/AS20_031125_trainingSingle6Tone2024_0_39.mat
2025-10-03 12:54:25,790 [INFO]   BH/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.bin
2025-10-03 12:54:36,322 [INFO]   BH/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.meta
2025-10-03 12:54:36,402 [INFO]   BH/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.bin
2025-10-03 12:54:49,357 [INFO]   BH/AS20-minimal2/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.meta
2025-10-03 12:54:49,444 [INFO] Setting group and other permissions for session dir /vol/cortex/cd4/geffenlab/raw_data/BH/AS20-minimal2/03112025:
2025-10-03 12:54:49,521 [INFO] [chan 1] sftp session closed.
2025-10-03 12:54:49,522 [INFO] OK.
```

## Options

The example above used several default options like the cortex host address, the local directories to search for behavior and spikeglx files, and the lab's assigned data directory on cortex.
All of these can be modified from the command line as needed.  For details please see:

```
python geffenlab-ephys-pipeline/scripts/upload_data.py --help
```

# Download results from cortex

This repo has a Python script [download_results.py](./scripts/download_results.py) that should help downloading pipeline results from cortex to your local machine.  Internally this uses `ssh` to connect to cortex, and the Python wrapper should add convenience.

You might have used this already as part of your [cortex-first-run.md](./cortex-first-run.md).

Run this script from the WSL environment of your local lab machine:

```
cd ~
conda activate geffen-pipelines

python geffenlab-ephys-pipeline/scripts/download_results.py
```

This will prompt you for the experimenter initials, subject id, and session date you want to download.  It will also ask for your cortex credentials.  For example:

```
2025-10-03 15:32:25,755 [INFO] Downloading files to local root: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs
2025-10-03 15:32:25,755 [INFO] Downloading files from remote host: 128.91.19.199
2025-10-03 15:32:25,755 [INFO] Downloading files from remote processed data root: /vol/cortex/cd4/geffenlab/processed_data
2025-10-03 15:32:25,755 [INFO] Downloading files from remote analysis root: /vol/cortex/cd4/geffenlab/analysis
2025-10-03 15:32:25,755 [INFO] Downloading processing logs that match patterns: ['*.log', '*.md']
2025-10-03 15:32:25,755 [INFO] Downloading processed data subdirs: ['nextflow', 'sorted/nextflow', 'sorted/visualization']
Experimenter initials: BH
2025-10-03 15:32:29,387 [INFO] Downloading files for experimenter: BH

Subject ID: AS20-minimal2
2025-10-03 15:32:33,406 [INFO] Downloading files for subject id: AS20-minimal2

Session date MMDDYYYY: 03112025
2025-10-03 15:32:37,427 [INFO] Downloading files for session date: 03112025 (2025-03-11)

Remote username: ben
2025-10-03 15:32:38,939 [INFO] Downloading files as remote user: ben

Password for remote user ben:
```

It will summarize what it finds in the session's analysis subdirectory on cortex, and download all of these files:

```
2025-10-03 15:32:52,850 [INFO] Checking for remote analysis session directory /vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal2/03112025:
synthesis
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal2/03112025/synthesis/figures/AS20-minimal2-03112025_demo.png
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal2/03112025/synthesis/figures/AS20-minimal2-03112025_neurons_1.png
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal2/03112025/synthesis/BH_AS20-minimal2_03112025_summary.pkl

2025-10-03 15:32:53,120 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/synthesis/figures/AS20-minimal2-03112025_demo.png
2025-10-03 15:32:53,158 [INFO] [chan 2] Opened sftp connection (server version 3)
2025-10-03 15:32:53,263 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/synthesis/figures/AS20-minimal2-03112025_neurons_1.png
2025-10-03 15:32:53,333 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/synthesis/BH_AS20-minimal2_03112025_summary.pkl
```

It will summarize what it finds in the sessions's processed data subdirectory on cortex:

```
2025-10-03 15:32:53,430 [INFO] Checking for remote processed data session directory /vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal2/03112025:
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
2025-10-03 15:32:53,869 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/main_20251003T190321UTC_nextflow.log
2025-10-03 15:32:53,890 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/main_20251003T190321UTC_run_pipeline.log
2025-10-03 15:32:54,235 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/main_20251003T190321UTC_process_detail.md
2025-10-03 15:32:53,999 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/main_multi_backend_20251003T175141UTC_nextflow.log
2025-10-03 15:32:54,021 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/main_multi_backend_20251003T175141UTC_run_pipeline.log
2025-10-03 15:32:54,276 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/main_multi_backend_20251003T175141UTC_process_detail.md
```

It will download selected subdirectories from within the session's processed data directory.
These should contain Nexflow reports and AIND pipeline diagnostic plots.

`nextflow`
```
2025-10-03 15:32:54,295 [INFO] Checking for processed data subdir nextflow:
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal2/03112025/nextflow/dag.html
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal2/03112025/nextflow/report.html
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal2/03112025/nextflow/trace.txt
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal2/03112025/nextflow/timeline.html
2025-10-03 15:32:54,320 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/nextflow/dag.html
2025-10-03 15:32:54,373 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/nextflow/report.html
2025-10-03 15:32:54,457 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/nextflow/trace.txt
2025-10-03 15:32:54,475 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/nextflow/timeline.html
```

`sorted/nextflow`
```
2025-10-03 15:32:54,542 [INFO] Checking for processed data subdir sorted/nextflow:
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal2/03112025/sorted/nextflow/dag.html
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal2/03112025/sorted/nextflow/report.html
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal2/03112025/sorted/nextflow/trace.txt
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal2/03112025/sorted/nextflow/timeline.html
2025-10-03 15:32:54,557 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/sorted/nextflow/dag.html
2025-10-03 15:32:54,618 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/sorted/nextflow/report.html
2025-10-03 15:32:54,709 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/sorted/nextflow/trace.txt
2025-10-03 15:32:54,736 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/sorted/nextflow/timeline.html
```

`sorted/visualization`
```
2025-10-03 15:32:54,820 [INFO] Checking for processed data subdir sorted/visualization:
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal2/03112025/sorted/visualization/block0_imec0.ap_recording1/traces_proc_seg0.png
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal2/03112025/sorted/visualization/block0_imec0.ap_recording1/motion.png
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal2/03112025/sorted/visualization/block0_imec0.ap_recording1/traces_full_seg0.png
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal2/03112025/sorted/visualization/block0_imec0.ap_recording1/drift_map.png
2025-10-03 15:32:54,841 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/sorted/visualization/block0_imec0.ap_recording1/traces_proc_seg0.png
2025-10-03 15:32:55,022 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/sorted/visualization/block0_imec0.ap_recording1/motion.png
2025-10-03 15:32:55,095 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/sorted/visualization/block0_imec0.ap_recording1/traces_full_seg0.png
2025-10-03 15:32:55,205 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/BH/AS20-minimal2/03112025/sorted/visualization/block0_imec0.ap_recording1/drift_map.png
```

When finished you should be able to open `ephys-pipeline-outputs` on the Windows desktop and browse to the results.

## Options

The example above used several default options like the cortex host address, the local directory to receive results, and which subfolders to download for the given session.
All of these can be modified from the command line as needed.  For details please see:

```
python geffenlab-ephys-pipeline/scripts/download_results.py --help
```
