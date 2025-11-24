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
```

Based on the experimenter, subject, and session date(s), the script will search your local `pipeline-results/` folder for the `analysis/` subdirectory of the specified session (s).

```
```

From all the files found, the script can use the optional qualifier to further restrict which files will be uploaded.  When the qualifier is provided, only files that contain the qualifier in their name will be uploaded.  For example, the qualifier "training" could be used to select "training" files but ignore "testing" files.

Before uploading, the script will show which files it plans to upload back to cortex and prompt for your confirmation.

```
```

You must type `yes` to proceed.  Otherwise the script will exit before uploading.
If you do type `yes` the script will prompt for your cortex user password and, then upload each file to cortex:

```

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
