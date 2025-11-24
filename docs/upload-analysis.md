# Cortex Upload Analysis

This doc should help you upload session analysis results from a local lab machine, back to cortex.

First, you'll need to do the one-time [cortex user setup](./cortex-user-setup.md) for your cortex user account and local lab machine.

You'll also need to get process some data on cortex and download the results to your local `pipeline-results/` folder.
See [download-results.md](download-results.md)

## Upload analysis results to cortex

This repo has a Python script [upload_analysis.py](../scripts/upload_analysis.py) that should help uploading analysis results from your local lab machine to cortex.  Internally this uses `ssh` to connect to cortex using your own user credentials.

Run this script from the WSL environment of your local lab machine:

```
# Go to the directory that contains your pipeline-results/ folder of results.
# This is one example:
cd /mnt/c/Users/labuser/Desktop
conda activate geffen-pipelines

# Run the analysis upload Python script.
python ~/geffenlab-ephys-pipeline/scripts/upload_analysis.py
```

This will prompt you for the experimenter initials, subject id, and session date(s) that you want to upload.  You can optionally specify a qualifier to further narrow down which files are uploaded.  For example:

```
2025-11-24 16:37:40,158 [INFO] Uploading files from local analysis root: /mnt/c/Users/labuser/Desktop/pipeline-results/analysis
2025-11-24 16:37:40,158 [INFO] Uploading files to remote host: 128.91.19.199
2025-11-24 16:37:40,158 [INFO] Uploading files to remote analysis root: /vol/cortex/cd4/geffenlab/analysis
Experimenter initials: BH
2025-11-24 16:37:42,614 [INFO] Uploading files for experimenter: BH
Subject ID: AS20-minimal3
2025-11-24 16:37:47,784 [INFO] Uploading files for subject id: AS20-minimal3
Session date MMDDYYYY (multiple dates may be separated by spaces): 03112025
2025-11-24 16:37:52,213 [INFO] Uploading files for session date(s): ['2025-03-11']
Qualifier like 'training','ap.bin', 'recording1', etc.  Leave blank to upload all:
2025-11-24 16:37:53,701 [INFO] Uploading all files.
Remote username: ben
2025-11-24 16:37:55,323 [INFO] Uploading files as remote user: ben
```

Based on the experimenter, subject, and session date(s), the script will search your local `pipeline-results/` folder for the `analysis/` subdirectory of the specified session(s).

```
2025-11-24 16:37:55,323 [INFO] Looking for session date: 2025-03-11 AKA 03112025
2025-11-24 16:37:55,324 [INFO] Looking in local analysis subdir: /mnt/c/Users/labuser/Desktop/pipeline-results/analysis/BH/AS20-minimal3/03112025
2025-11-24 16:37:55,492 [INFO]   BH/AS20-minimal3/03112025/run_phy_20251124T184018UTC.log
2025-11-24 16:37:55,492 [INFO]   BH/AS20-minimal3/03112025/run_phy_20251124T213613UTC.log
2025-11-24 16:37:55,493 [INFO]   BH/AS20-minimal3/03112025/run_phy_20251124T213649UTC.log
... etc ...
2025-11-24 16:37:55,503 [INFO]   BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/params.py
2025-11-24 16:37:55,504 [INFO]   BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/phy.log
2025-11-24 16:37:55,504 [INFO]   BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/run_phy.log
2025-11-24 16:37:55,504 [INFO]   BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/similar_templates.npy
... etc ...
```

From all the files found, the script can use the optional qualifier to further restrict which files will be uploaded.  When the qualifier is provided, only files that contain the qualifier in their name will be uploaded.  For example, the qualifier "training" could be used to select "training" files but ignore "testing" files.

Before uploading, the script will show which files it plans to upload back to cortex and prompt for your confirmation.

```
2025-11-24 16:37:55,512 [INFO] Planning to create 224 files in remote dir /vol/cortex/cd4/geffenlab/analysis:
2025-11-24 16:37:55,513 [INFO]   BH/AS20-minimal3/03112025/run_phy_20251124T184018UTC.log
2025-11-24 16:37:55,513 [INFO]   BH/AS20-minimal3/03112025/run_phy_20251124T213613UTC.log
2025-11-24 16:37:55,513 [INFO]   BH/AS20-minimal3/03112025/run_phy_20251124T213649UTC.log
... etc ...
2025-11-24 16:37:55,518 [INFO]   BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/params.py
2025-11-24 16:37:55,518 [INFO]   BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/phy.log
2025-11-24 16:37:55,518 [INFO]   BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/run_phy.log
2025-11-24 16:37:55,518 [INFO]   BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/similar_templates.npy
... etc ...
Do you want to upload these 224 files?  Type 'yes' to proceed: yes
```

You must type `yes` to proceed.  Otherwise the script will exit before uploading.
If you do type `yes` the script will prompt for your cortex user password and, then upload each file to cortex:

```
2025-11-24 16:38:14,838 [WARNING] Proceeding to upload files.
Password for remote user ben:
2025-11-24 16:38:20,713 [INFO] Connecting to remote host: 128.91.19.199.
2025-11-24 16:38:30,761 [INFO] Connected (version 2.0, client OpenSSH_8.9p1)
2025-11-24 16:38:30,875 [INFO] Authentication (password) successful!
2025-11-24 16:38:30,875 [INFO] Uploading to /vol/cortex/cd4/geffenlab/analysis:
2025-11-24 16:38:30,875 [INFO]   BH/AS20-minimal3/03112025/run_phy_20251124T184018UTC.log
2025-11-24 16:38:31,901 [INFO] [chan 1] Opened sftp connection (server version 3)
2025-11-24 16:38:31,917 [INFO]   BH/AS20-minimal3/03112025/run_phy_20251124T213613UTC.log
2025-11-24 16:38:31,980 [INFO]   BH/AS20-minimal3/03112025/run_phy_20251124T213649UTC.log
... etc ...
2025-11-24 16:38:42,521 [INFO]   BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/params.py
2025-11-24 16:38:42,601 [INFO]   BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/phy.log
2025-11-24 16:38:42,685 [INFO]   BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/run_phy.log
2025-11-24 16:38:42,776 [INFO]   BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/similar_templates.npy
... etc ...
2025-11-24 16:38:51,424 [INFO] Setting 'group' and 'other' permissions for session dir /vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025:
2025-11-24 16:38:51,540 [INFO] [chan 1] sftp session closed.
2025-11-24 16:38:51,540 [INFO] OK.
```

## Options

The example above used several default options like the cortex host address, the local directories to search for behavior and spikeglx files, and the lab's assigned data directory on cortex.
All of these can be modified from the command line as needed.

You can also specify many values like `--experimenter`, `--subject`, `--date`, and `--qualifier` on the command line instead of waiting for the script to prompt you interactively.  The only argument you can not speicy on the command line is your cortex user password -- this is to prevent your password from being saved into your terminal command history.

For details of command line options please see:

```
python geffenlab-ephys-pipeline/scripts/upload_analysis.py --help
```

## Uploading multiple dates at once

For the `--date` command line option, or when prompted interactively for session dates, you can provide one or more session dates separated by spaces for the script to search and upload.

For example:

```
python geffenlab-ephys-pipeline/scripts/upload_analysis.py --date 03112025 03122025 03132025
```

```
Session date MMDDYYYY (multiple dates may be separated by spaces): 03112025 03122025 03132025
```
