# Archiving Data to S3

This doc should help you archive session raw data from a cortex to the lab's S3 bucket.

First, you'll need to do the one-time [cortex user setup](./cortex-user-setup.md) for your cortex user account and local lab machine.

## Archive raw data to S3

This repo has a Python script [archive.py](../scripts/archive_data.py) that should help archiving data from cortex to the lab's S3 bucket.

Connect to cortex via remote desktop and open a terminal window and run this script:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python ~/geffenlab-ephys-pipeline/scripts/archive_data.py --delete
```

The `--delete` flag means files data will be deleted from cortex once it's succesfully archived to S3.  If you don't supply this flag, the files will be kept on cortex even after archiving.

You can also use the `--dry-run` flag to see what the script would do, without committing data to S3 or deleting anything.

The script will prompt you for the experimenter initials, subject id, and session date(s) that you want to archive.  For example:

```
2026-01-22 16:21:42,606 [INFO] Archiving files within raw data root: /vol/cortex/cd4/geffenlab/raw_data
Experimenter initials: BH
2026-01-22 16:21:44,836 [INFO] Archiving files for experimenter: BH
Subject ID: AS20-archive-test
2026-01-22 16:21:55,366 [INFO] Archiving files for subject id: AS20-archive-test
Session date MMDDYYYY (multiple dates may be separated by spaces): 03112025
2026-01-22 16:22:03,592 [INFO] Archiving files for session date(s): ['2025-03-11']
Qualifier like 'training','ap.bin', 'recording1', etc.  Leave blank to upload all: 
2026-01-22 16:22:04,896 [INFO] Archiving all files
2026-01-22 16:22:04,896 [INFO] Using S3 bucket: upenn-research.geffen-lab-01.us-east-1
2026-01-22 16:22:04,897 [INFO] Using S3 bucket path prefix: cortex/raw_data
2026-01-22 16:22:04,897 [INFO] Using S3 storage class: DEEP_ARCHIVE
2026-01-22 16:22:04,897 [INFO] Using AWS credentials from: /vol/cortex/cd4/geffenlab/.aws/credentials
2026-01-22 16:22:04,897 [INFO] Using AWS config from: /vol/cortex/cd4/geffenlab/.aws/config
2026-01-22 16:22:04,897 [WARNING] Deleting local files after archiving.
```

Based on the experimenter initials, subject id, session date(s), and optional qualifier, the script will search the local `raw_data` directory for files to archive.

From all the files found, the script can use the optional qualifier to further restrict which files will be uploaded.  When the qualifier is provided, only files that contain the qualifier in their name will be uploaded.  For example, the qualifier "training" could be used to select "training" files but ignore "testing" files.

Before archiving, the script will show which files it plans to archive to S3 and prompt for your confirmation.

```
2026-01-22 16:22:04,897 [INFO] Looking for session date: 2025-03-11 AKA 03112025
2026-01-22 16:22:04,898 [INFO] Found 10 files within: /vol/cortex/cd4/geffenlab/raw_data/BH/AS20-archive-test/03112025
2026-01-22 16:22:04,899 [INFO] Planning to archive 10 files within /vol/cortex/cd4/geffenlab/raw_data/BH/AS20-archive-test:
2026-01-22 16:22:04,899 [INFO]   03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.bin
2026-01-22 16:22:04,899 [INFO]   03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.meta
2026-01-22 16:22:04,899 [INFO]   03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.meta
2026-01-22 16:22:04,899 [INFO]   03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.bin
2026-01-22 16:22:04,899 [INFO]   03112025/ecephys/another_session_test_g0/another_session_test_g0_t0.nidq.meta
2026-01-22 16:22:04,899 [INFO]   03112025/ecephys/another_session_test_g0/another_session_test_g0_t0.nidq.bin
2026-01-22 16:22:04,899 [INFO]   03112025/ecephys/another_session_test_g0/another_session_test_g0_imec0/another_session_test_g0_t0.imec0.ap.meta
2026-01-22 16:22:04,899 [INFO]   03112025/ecephys/another_session_test_g0/another_session_test_g0_imec0/another_session_test_g0_t0.imec0.ap.bin
2026-01-22 16:22:04,900 [INFO]   03112025/behavior/AS20_031125_trainingSingle6Tone2024_0_39.mat
2026-01-22 16:22:04,900 [INFO]   03112025/behavior/AS20_031125_trainingSingle6Tone2024_0_39.txt
Do you want to archive these 10 files?  Type 'yes' to proceed: yes
```

You must type `yes` to proceed.  Otherwise the script will exit before archiving.
If you do type `yes` the script will upload files to S3.:


```
2026-01-22 16:22:14,656 [WARNING] Proceeding to archive files.
2026-01-22 16:22:14,682 [INFO] Found credentials in shared credentials file: /vol/cortex/cd4/geffenlab/.aws/credentials
2026-01-22 16:22:14,809 [INFO] Archiving s3://upenn-research.geffen-lab-01.us-east-1/cortex/raw_data/BH/AS20-archive-test/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.bin
2026-01-22 16:22:26,009 [INFO] Archiving s3://upenn-research.geffen-lab-01.us-east-1/cortex/raw_data/BH/AS20-archive-test/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.meta
2026-01-22 16:22:26,083 [INFO] Archiving s3://upenn-research.geffen-lab-01.us-east-1/cortex/raw_data/BH/AS20-archive-test/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.meta
2026-01-22 16:22:26,176 [INFO] Archiving s3://upenn-research.geffen-lab-01.us-east-1/cortex/raw_data/BH/AS20-archive-test/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.bin
2026-01-22 16:22:40,796 [INFO] Archiving s3://upenn-research.geffen-lab-01.us-east-1/cortex/raw_data/BH/AS20-archive-test/03112025/ecephys/another_session_test_g0/another_session_test_g0_t0.nidq.meta
2026-01-22 16:22:40,874 [INFO] Archiving s3://upenn-research.geffen-lab-01.us-east-1/cortex/raw_data/BH/AS20-archive-test/03112025/ecephys/another_session_test_g0/another_session_test_g0_t0.nidq.bin
2026-01-22 16:22:52,252 [INFO] Archiving s3://upenn-research.geffen-lab-01.us-east-1/cortex/raw_data/BH/AS20-archive-test/03112025/ecephys/another_session_test_g0/another_session_test_g0_imec0/another_session_test_g0_t0.imec0.ap.meta
2026-01-22 16:22:52,324 [INFO] Archiving s3://upenn-research.geffen-lab-01.us-east-1/cortex/raw_data/BH/AS20-archive-test/03112025/ecephys/another_session_test_g0/another_session_test_g0_imec0/another_session_test_g0_t0.imec0.ap.bin
2026-01-22 16:23:06,292 [INFO] Archiving s3://upenn-research.geffen-lab-01.us-east-1/cortex/raw_data/BH/AS20-archive-test/03112025/behavior/AS20_031125_trainingSingle6Tone2024_0_39.mat
2026-01-22 16:23:06,353 [INFO] Archiving s3://upenn-research.geffen-lab-01.us-east-1/cortex/raw_data/BH/AS20-archive-test/03112025/behavior/AS20_031125_trainingSingle6Tone2024_0_39.txt
2026-01-22 16:23:06,414 [INFO] Archived 10 files
```

If you provided the `--delete` flag, the script will then delete the archived files from cortex.

```
2026-01-22 16:23:06,414 [WARNING] Proceeding to delete local files.
2026-01-22 16:23:06,414 [INFO] Deleting BH/AS20-archive-test/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.bin
2026-01-22 16:23:06,719 [INFO] Deleting BH/AS20-archive-test/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.nidq.meta
2026-01-22 16:23:06,719 [INFO] Deleting BH/AS20-archive-test/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.meta
2026-01-22 16:23:06,719 [INFO] Deleting BH/AS20-archive-test/03112025/ecephys/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_t0.imec0.ap.bin
2026-01-22 16:23:07,165 [INFO] Deleting BH/AS20-archive-test/03112025/ecephys/another_session_test_g0/another_session_test_g0_t0.nidq.meta
2026-01-22 16:23:07,165 [INFO] Deleting BH/AS20-archive-test/03112025/ecephys/another_session_test_g0/another_session_test_g0_t0.nidq.bin
2026-01-22 16:23:07,509 [INFO] Deleting BH/AS20-archive-test/03112025/ecephys/another_session_test_g0/another_session_test_g0_imec0/another_session_test_g0_t0.imec0.ap.meta
2026-01-22 16:23:07,510 [INFO] Deleting BH/AS20-archive-test/03112025/ecephys/another_session_test_g0/another_session_test_g0_imec0/another_session_test_g0_t0.imec0.ap.bin
2026-01-22 16:23:07,932 [INFO] Deleting BH/AS20-archive-test/03112025/behavior/AS20_031125_trainingSingle6Tone2024_0_39.mat
2026-01-22 16:23:07,932 [INFO] Deleting BH/AS20-archive-test/03112025/behavior/AS20_031125_trainingSingle6Tone2024_0_39.txt
```

The files for the chosen session(s) should then be present in the lab's S3 bucket.  If you have a Penn AWS account and permission to view the lab's bucket, you should be able to see the archived files in the AWS web UI.  For example: [s3://upenn-research.geffen-lab-01.us-east-1/cortex/raw_data/BH/AS20-archive-test/03112025](https://us-east-1.console.aws.amazon.com/s3/buckets/upenn-research.geffen-lab-01.us-east-1?region=us-east-1&prefix=cortex/raw_data/BH/AS20-archive-test/03112025/&showversions=false).
