# Cortex Moving Data

This doc should help you download pipelines results from cortex to your local machine.

First, you'll need to do the one-time [cortex user setup](./cortex-user-setup.md) for your cortex user account and local lab machine.

# Download results from cortex

This repo has a Python script [download_results.py](./scripts/download_results.py) that should help downloading pipeline results from cortex to your local machine.  Internally this uses `ssh` to connect to cortex using your own user credentials.

Run this script from the WSL environment of your local lab machine:

```
# Go to the directory that will contain your `pipeline-results/` folder of results.
# This is one example:
cd /mnt/c/Users/labuser/Desktop
conda activate geffen-pipelines

# Run our results download Python script.
python ~/geffenlab-ephys-pipeline/scripts/download_results.py
```

This will prompt you for the experimenter initials, subject id, and session date you want to download.  It will also ask for your cortex credentials.  For example:

```
2025-11-24 14:22:42,898 [INFO] Downloading files to local root: /mnt/c/Users/labuser/Desktop/pipeline-results
2025-11-24 14:22:42,898 [INFO] Downloading files from remote host: 128.91.19.199
2025-11-24 14:22:42,898 [INFO] Downloading files from remote processed data root: /vol/cortex/cd4/geffenlab/processed_data
2025-11-24 14:22:42,898 [INFO] Downloading files from remote analysis root: /vol/cortex/cd4/geffenlab/analysis
2025-11-24 14:22:42,898 [INFO] Downloading processed_data subdirs: ['logs', 'sorted/nextflow', 'sorted/visualization']
Experimenter initials: BH
2025-11-24 14:23:02,662 [INFO] Downloading files for experimenter: BH
Subject ID: AS20-minimal3
2025-11-24 14:23:10,194 [INFO] Downloading files for subject id: AS20-minimal3
Session date MMDDYYYY: 03112025
2025-11-24 14:23:22,345 [INFO] Downloading files for session date: 03112025 (2025-03-11)
Remote username: ben
2025-11-24 14:23:24,530 [INFO] Downloading files as remote user: ben
Password for remote user ben:
2025-11-24 14:23:29,303 [INFO] Connecting to remote host: 128.91.19.199.
2025-11-24 14:23:40,001 [INFO] Connected (version 2.0, client OpenSSH_8.9p1)
2025-11-24 14:23:40,124 [INFO] Authentication (password) successful!
```

It will summarize what it finds in the session's `analysis/` subdirectory on cortex, and download all of these files:

```
2025-11-24 14:23:40,125 [INFO] Checking for remote analysis session directory /vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025:
phy-export
run_phy_20251124T184018UTC.log
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/params.py
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/templates.npy
... etc ...
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/run_phy_20251124T184018UTC.log

2025-11-24 14:23:41,837 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/bombcell/TODO.txt
2025-11-24 14:23:41,900 [INFO] [chan 2] Opened sftp connection (server version 3)
2025-11-24 14:23:42,030 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/params.py
2025-11-24 14:23:43,255 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_templates.npy
... etc ...
2025-11-24 14:23:54,502 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/run_phy_20251124T184018UTC.log
```

It will also check selected subdirs of the session's `processed_data/` subdir, and summarize and download what if finds there:


```

```

When finished you should be able to browse your local `pipeline-results/` folder and see all the results.

## Options

The example above used several default options like the cortex host address, the local directory to receive results, and which subfolders to download for the given session.
All of these can be modified from the command line as needed.  For details please see:

```
python geffenlab-ephys-pipeline/scripts/download_results.py --help
```





2025-11-24 14:23:40,125 [INFO] Checking for remote analysis session directory /vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025:
phy-export
run_phy_20251124T184018UTC.log
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/bombcell/TODO.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/params.py
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_exp_decay.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_spread.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/whitening_mat_inv.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_amplitude_cv_median.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_sync_spike_4.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_group.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_isolation_distance.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_repolarization_slope.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_amplitude_cutoff.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_times_original.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_templates.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_silhouette.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_peak_to_valley.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/template_ind.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_amplitude_median.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_decoder_label.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_si_unit_id.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_amplitude_cv_range.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/similar_templates.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_times_adj.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_presence_ratio.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_velocity_above.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_recovery_slope.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_num_negative_peaks.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_rp_contamination.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/channel_map_si.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_times_sec_adj.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_isi_violations_count.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_KSLabel.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/templates.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_decoder_probability.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_info.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_original_cluster_id.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_channel_group.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/channel_map.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_rp_violations.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_KSLabel_repeat.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_peak_trough_ratio.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_nn_hit_rate.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_default_qc.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_Amplitude.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_drift_std.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_isi_violations_ratio.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_velocity_below.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/amplitudes.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/channel_positions.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_times.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_drift_ptp.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_drift_mad.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_times_sec_original.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_d_prime.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_nn_miss_rate.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_sync_spike_2.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_l_ratio.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_firing_range.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_sync_spike_8.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/run_phy.log
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/phy.log
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_sliding_rp_violation.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_ContamPct.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_snr.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/channel_groups.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_half_width.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_num_positive_peaks.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_clusters.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_si_unit_ids.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/state.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/new_cluster_id.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/spikes_per_cluster.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/3e309c3fa2a77f86255f699f77c2e64e/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/3e309c3fa2a77f86255f699f77c2e64e/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/3d29da0ab7cb36e3138982e8de51f646/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/3d29da0ab7cb36e3138982e8de51f646/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/func_code.py
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/f4aa1cb556963f432a1507fb84a7ba28/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/f4aa1cb556963f432a1507fb84a7ba28/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/0734e9d63482efe69dc0c2a8fc97ba26/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/0734e9d63482efe69dc0c2a8fc97ba26/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/0b9134e1227f345878c392523b1757eb/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/0b9134e1227f345878c392523b1757eb/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/b5d623512c800d9456990f383401e450/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/b5d623512c800d9456990f383401e450/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/e4a5a1b8a60652d0e7b1fb473b8e7665/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/e4a5a1b8a60652d0e7b1fb473b8e7665/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/b3bbb71634ae6882133a96f96a3b17c6/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/b3bbb71634ae6882133a96f96a3b17c6/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/func_code.py
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/9e67d6de89ae4bd28b4dcb6928325364/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/9e67d6de89ae4bd28b4dcb6928325364/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/55477e2499bee75bcd01ea1f33720e13/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/55477e2499bee75bcd01ea1f33720e13/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/fa17eedbb478a3eacecdc7bdace173fa/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/fa17eedbb478a3eacecdc7bdace173fa/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/b866e815fc409da16994fd11bc0f94ee/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/b866e815fc409da16994fd11bc0f94ee/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/func_code.py
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/2144a3bd0001e8f27aafcda74dea94f7/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/2144a3bd0001e8f27aafcda74dea94f7/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/af9f59659bde2567ce27df8f4b6d4fae/output.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/af9f59659bde2567ce27df8f4b6d4fae/metadata.json
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_probe_depth.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base._get_mean_waveforms.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.template.gui.get_template_amplitude.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_best_channel.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.template.gui.get_best_channels.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_template_for_cluster.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_template_counts.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_cluster_amplitude.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_channel_shank.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_mean_firing_rate.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_mean_spike_template_amplitudes.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.peak_channel_similarity.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base._get_template_waveforms.pkl
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/TPrime.log
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xa_0_500.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xd_8_3_0.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xid_8_2_1p7.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xia_1_0.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/tprime/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xid_8_3_5.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/catgt/CatGT.log
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xa_0_500.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xd_8_3_0.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_ct_offsets.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.meta
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.imec0.ap.xd_384_6_500.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.imec0.ap.meta
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xid_8_2_1p7.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xd_8_4_500.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_fyi.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xia_1_0.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xid_8_3_5.txt
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/params.py
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_exp_decay.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_spread.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/whitening_mat_inv.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_amplitude_cv_median.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_sync_spike_4.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_group.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_isolation_distance.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_repolarization_slope.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_amplitude_cutoff.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/spike_templates.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_silhouette.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_peak_to_valley.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/template_ind.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_amplitude_median.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_decoder_label.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_amplitude_cv_range.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/similar_templates.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_presence_ratio.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_velocity_above.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_recovery_slope.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_num_negative_peaks.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_rp_contamination.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/channel_map_si.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_isi_violations_count.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_KSLabel.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/templates.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_decoder_probability.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_info.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_original_cluster_id.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_channel_group.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/channel_map.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_rp_violations.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_KSLabel_repeat.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_peak_trough_ratio.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_nn_hit_rate.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_default_qc.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_Amplitude.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_drift_std.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_isi_violations_ratio.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_velocity_below.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/amplitudes.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/channel_positions.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/spike_times.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_drift_ptp.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_drift_mad.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_d_prime.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_nn_miss_rate.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_sync_spike_2.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_l_ratio.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_firing_range.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_sync_spike_8.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_sliding_rp_violation.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_ContamPct.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_snr.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/channel_groups.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_half_width.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_num_positive_peaks.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/spike_clusters.npy
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_si_unit_ids.tsv
/vol/cortex/cd4/geffenlab/analysis/BH/AS20-minimal3/03112025/run_phy_20251124T184018UTC.log
2025-11-24 14:23:41,837 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/bombcell/TODO.txt
2025-11-24 14:23:41,900 [INFO] [chan 2] Opened sftp connection (server version 3)
2025-11-24 14:23:42,030 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/params.py
2025-11-24 14:23:42,132 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_exp_decay.tsv
2025-11-24 14:23:42,209 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_spread.tsv
2025-11-24 14:23:42,239 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/whitening_mat_inv.npy
2025-11-24 14:23:42,491 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_amplitude_cv_median.tsv
2025-11-24 14:23:42,589 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_sync_spike_4.tsv
2025-11-24 14:23:42,690 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_group.tsv
2025-11-24 14:23:42,793 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_isolation_distance.tsv
2025-11-24 14:23:42,906 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_repolarization_slope.tsv
2025-11-24 14:23:42,987 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_amplitude_cutoff.tsv
2025-11-24 14:23:43,080 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_times_original.npy
2025-11-24 14:23:43,255 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_templates.npy
2025-11-24 14:23:43,385 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_silhouette.tsv
2025-11-24 14:23:43,460 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_peak_to_valley.tsv
2025-11-24 14:23:43,490 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/template_ind.npy
2025-11-24 14:23:43,588 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_amplitude_median.tsv
2025-11-24 14:23:43,640 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_decoder_label.tsv
2025-11-24 14:23:43,671 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_si_unit_id.tsv
2025-11-24 14:23:43,767 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_amplitude_cv_range.tsv
2025-11-24 14:23:43,834 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/similar_templates.npy
2025-11-24 14:23:43,923 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_times_adj.npy
2025-11-24 14:23:44,052 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_presence_ratio.tsv
2025-11-24 14:23:44,116 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_velocity_above.tsv
2025-11-24 14:23:44,148 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_recovery_slope.tsv
2025-11-24 14:23:44,194 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_num_negative_peaks.tsv
2025-11-24 14:23:44,225 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_rp_contamination.tsv
2025-11-24 14:23:44,286 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/channel_map_si.npy
2025-11-24 14:23:44,317 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_times_sec_adj.npy
2025-11-24 14:23:44,537 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_isi_violations_count.tsv
2025-11-24 14:23:44,568 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_KSLabel.tsv
2025-11-24 14:23:44,645 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/templates.npy
2025-11-24 14:23:44,903 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_decoder_probability.tsv
2025-11-24 14:23:44,928 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_info.tsv
2025-11-24 14:23:45,009 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_original_cluster_id.tsv
2025-11-24 14:23:45,036 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_channel_group.tsv
2025-11-24 14:23:45,096 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/channel_map.npy
2025-11-24 14:23:45,174 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_rp_violations.tsv
2025-11-24 14:23:45,201 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_KSLabel_repeat.tsv
2025-11-24 14:23:45,280 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_peak_trough_ratio.tsv
2025-11-24 14:23:45,359 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_nn_hit_rate.tsv
2025-11-24 14:23:45,386 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_default_qc.tsv
2025-11-24 14:23:45,453 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_Amplitude.tsv
2025-11-24 14:23:45,501 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_drift_std.tsv
2025-11-24 14:23:45,582 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_isi_violations_ratio.tsv
2025-11-24 14:23:45,630 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_velocity_below.tsv
2025-11-24 14:23:45,714 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/amplitudes.npy
2025-11-24 14:23:45,813 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/channel_positions.npy
2025-11-24 14:23:45,840 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_times.npy
2025-11-24 14:23:45,991 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_drift_ptp.tsv
2025-11-24 14:23:46,020 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_drift_mad.tsv
2025-11-24 14:23:46,054 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_times_sec_original.npy
2025-11-24 14:23:46,219 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_d_prime.tsv
2025-11-24 14:23:46,281 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_nn_miss_rate.tsv
2025-11-24 14:23:46,311 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_sync_spike_2.tsv
2025-11-24 14:23:46,370 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_l_ratio.tsv
2025-11-24 14:23:46,451 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_firing_range.tsv
2025-11-24 14:23:46,536 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_sync_spike_8.tsv
2025-11-24 14:23:46,566 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/run_phy.log
2025-11-24 14:23:46,675 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/phy.log
2025-11-24 14:23:46,720 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_sliding_rp_violation.tsv
2025-11-24 14:23:46,751 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_ContamPct.tsv
2025-11-24 14:23:46,809 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_snr.tsv
2025-11-24 14:23:46,834 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/channel_groups.npy
2025-11-24 14:23:46,895 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_half_width.tsv
2025-11-24 14:23:46,928 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_num_positive_peaks.tsv
2025-11-24 14:23:46,983 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/spike_clusters.npy
2025-11-24 14:23:47,118 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/cluster_si_unit_ids.tsv
2025-11-24 14:23:47,169 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/state.json
2025-11-24 14:23:47,256 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/new_cluster_id.json
2025-11-24 14:23:47,348 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/spikes_per_cluster.pkl
2025-11-24 14:23:47,525 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/3e309c3fa2a77f86255f699f77c2e64e/output.pkl
2025-11-24 14:23:47,622 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/3e309c3fa2a77f86255f699f77c2e64e/metadata.json
2025-11-24 14:23:47,711 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/3d29da0ab7cb36e3138982e8de51f646/output.pkl
2025-11-24 14:23:47,766 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/3d29da0ab7cb36e3138982e8de51f646/metadata.json
2025-11-24 14:23:47,830 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/func_code.py
2025-11-24 14:23:47,903 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/f4aa1cb556963f432a1507fb84a7ba28/output.pkl
2025-11-24 14:23:47,987 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/f4aa1cb556963f432a1507fb84a7ba28/metadata.json
2025-11-24 14:23:48,027 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/0734e9d63482efe69dc0c2a8fc97ba26/output.pkl
2025-11-24 14:23:48,188 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/0734e9d63482efe69dc0c2a8fc97ba26/metadata.json
2025-11-24 14:23:48,332 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/0b9134e1227f345878c392523b1757eb/output.pkl
2025-11-24 14:23:48,440 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/0b9134e1227f345878c392523b1757eb/metadata.json
2025-11-24 14:23:48,651 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/b5d623512c800d9456990f383401e450/output.pkl
2025-11-24 14:23:48,733 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/TemplateMixin/get_spike_template_amplitudes/b5d623512c800d9456990f383401e450/metadata.json
2025-11-24 14:23:48,804 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/e4a5a1b8a60652d0e7b1fb473b8e7665/output.pkl
2025-11-24 14:23:48,870 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/e4a5a1b8a60652d0e7b1fb473b8e7665/metadata.json
2025-11-24 14:23:48,913 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/b3bbb71634ae6882133a96f96a3b17c6/output.pkl
2025-11-24 14:23:48,950 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/b3bbb71634ae6882133a96f96a3b17c6/metadata.json
2025-11-24 14:23:48,991 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/func_code.py
2025-11-24 14:23:49,033 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/9e67d6de89ae4bd28b4dcb6928325364/output.pkl
2025-11-24 14:23:49,082 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/9e67d6de89ae4bd28b4dcb6928325364/metadata.json
2025-11-24 14:23:49,127 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/55477e2499bee75bcd01ea1f33720e13/output.pkl
2025-11-24 14:23:49,164 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms_rate/55477e2499bee75bcd01ea1f33720e13/metadata.json
2025-11-24 14:23:49,233 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/fa17eedbb478a3eacecdc7bdace173fa/output.pkl
2025-11-24 14:23:49,321 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/fa17eedbb478a3eacecdc7bdace173fa/metadata.json
2025-11-24 14:23:49,364 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/b866e815fc409da16994fd11bc0f94ee/output.pkl
2025-11-24 14:23:49,446 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/b866e815fc409da16994fd11bc0f94ee/metadata.json
2025-11-24 14:23:49,533 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/func_code.py
2025-11-24 14:23:49,608 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/2144a3bd0001e8f27aafcda74dea94f7/output.pkl
2025-11-24 14:23:49,645 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/2144a3bd0001e8f27aafcda74dea94f7/metadata.json
2025-11-24 14:23:49,724 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/af9f59659bde2567ce27df8f4b6d4fae/output.pkl
2025-11-24 14:23:49,770 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/phy/apps/base/BaseController/_get_correlograms/af9f59659bde2567ce27df8f4b6d4fae/metadata.json
2025-11-24 14:23:49,824 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_probe_depth.pkl
2025-11-24 14:23:49,911 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base._get_mean_waveforms.pkl
2025-11-24 14:23:49,947 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.template.gui.get_template_amplitude.pkl
2025-11-24 14:23:50,036 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_best_channel.pkl
2025-11-24 14:23:50,072 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.template.gui.get_best_channels.pkl
2025-11-24 14:23:50,113 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_template_for_cluster.pkl
2025-11-24 14:23:50,150 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_template_counts.pkl
2025-11-24 14:23:50,186 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_cluster_amplitude.pkl
2025-11-24 14:23:50,222 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_channel_shank.pkl
2025-11-24 14:23:50,259 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_mean_firing_rate.pkl
2025-11-24 14:23:50,292 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.get_mean_spike_template_amplitudes.pkl
2025-11-24 14:23:50,325 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base.peak_channel_similarity.pkl
2025-11-24 14:23:50,358 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/phy/block0_imec0.ap_recording1/.phy/memcache/phy.apps.base._get_template_waveforms.pkl
2025-11-24 14:23:50,459 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/TPrime.log
2025-11-24 14:23:50,566 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xa_0_500.txt
2025-11-24 14:23:50,595 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xd_8_3_0.txt
2025-11-24 14:23:50,632 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xid_8_2_1p7.txt
2025-11-24 14:23:50,655 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xia_1_0.txt
2025-11-24 14:23:50,703 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/tprime/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xid_8_3_5.txt
2025-11-24 14:23:50,728 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/catgt/CatGT.log
2025-11-24 14:23:50,785 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xa_0_500.txt
2025-11-24 14:23:50,810 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xd_8_3_0.txt
2025-11-24 14:23:50,839 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_ct_offsets.txt
2025-11-24 14:23:50,907 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.meta
2025-11-24 14:23:50,936 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.imec0.ap.xd_384_6_500.txt
2025-11-24 14:23:50,995 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_imec0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.imec0.ap.meta
2025-11-24 14:23:51,030 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xid_8_2_1p7.txt
2025-11-24 14:23:51,096 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xd_8_4_500.txt
2025-11-24 14:23:51,127 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_fyi.txt
2025-11-24 14:23:51,179 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xia_1_0.txt
2025-11-24 14:23:51,210 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/catgt/catgt_AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0/AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0_tcat.nidq.xid_8_3_5.txt
2025-11-24 14:23:51,233 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/params.py
2025-11-24 14:23:51,308 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_exp_decay.tsv
2025-11-24 14:23:51,351 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_spread.tsv
2025-11-24 14:23:51,485 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/whitening_mat_inv.npy
2025-11-24 14:23:51,674 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_amplitude_cv_median.tsv
2025-11-24 14:23:51,715 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_sync_spike_4.tsv
2025-11-24 14:23:51,745 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_group.tsv
2025-11-24 14:23:51,804 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_isolation_distance.tsv
2025-11-24 14:23:51,840 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_repolarization_slope.tsv
2025-11-24 14:23:51,895 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_amplitude_cutoff.tsv
2025-11-24 14:23:51,929 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/spike_templates.npy
2025-11-24 14:23:52,059 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_silhouette.tsv
2025-11-24 14:23:52,115 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_peak_to_valley.tsv
2025-11-24 14:23:52,148 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/template_ind.npy
2025-11-24 14:23:52,223 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_amplitude_median.tsv
2025-11-24 14:23:52,253 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_decoder_label.tsv
2025-11-24 14:23:52,281 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_amplitude_cv_range.tsv
2025-11-24 14:23:52,320 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/similar_templates.npy
2025-11-24 14:23:52,381 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_presence_ratio.tsv
2025-11-24 14:23:52,430 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_velocity_above.tsv
2025-11-24 14:23:52,463 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_recovery_slope.tsv
2025-11-24 14:23:52,497 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_num_negative_peaks.tsv
2025-11-24 14:23:52,537 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_rp_contamination.tsv
2025-11-24 14:23:52,570 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/channel_map_si.npy
2025-11-24 14:23:52,626 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_isi_violations_count.tsv
2025-11-24 14:23:52,660 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_KSLabel.tsv
2025-11-24 14:23:52,700 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/templates.npy
2025-11-24 14:23:52,933 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_decoder_probability.tsv
2025-11-24 14:23:52,965 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_info.tsv
2025-11-24 14:23:52,999 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_original_cluster_id.tsv
2025-11-24 14:23:53,107 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_channel_group.tsv
2025-11-24 14:23:53,140 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/channel_map.npy
2025-11-24 14:23:53,174 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_rp_violations.tsv
2025-11-24 14:23:53,205 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_KSLabel_repeat.tsv
2025-11-24 14:23:53,243 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_peak_trough_ratio.tsv
2025-11-24 14:23:53,274 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_nn_hit_rate.tsv
2025-11-24 14:23:53,310 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_default_qc.tsv
2025-11-24 14:23:53,341 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_Amplitude.tsv
2025-11-24 14:23:53,373 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_drift_std.tsv
2025-11-24 14:23:53,401 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_isi_violations_ratio.tsv
2025-11-24 14:23:53,434 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_velocity_below.tsv
2025-11-24 14:23:53,469 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/amplitudes.npy
2025-11-24 14:23:53,591 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/channel_positions.npy
2025-11-24 14:23:53,629 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/spike_times.npy
2025-11-24 14:23:53,768 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_drift_ptp.tsv
2025-11-24 14:23:53,803 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_drift_mad.tsv
2025-11-24 14:23:53,834 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_d_prime.tsv
2025-11-24 14:23:53,895 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_nn_miss_rate.tsv
2025-11-24 14:23:53,992 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_sync_spike_2.tsv
2025-11-24 14:23:54,023 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_l_ratio.tsv
2025-11-24 14:23:54,055 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_firing_range.tsv
2025-11-24 14:23:54,088 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_sync_spike_8.tsv
2025-11-24 14:23:54,117 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_sliding_rp_violation.tsv
2025-11-24 14:23:54,150 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_ContamPct.tsv
2025-11-24 14:23:54,186 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_snr.tsv
2025-11-24 14:23:54,215 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/channel_groups.npy
2025-11-24 14:23:54,269 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_half_width.tsv
2025-11-24 14:23:54,307 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_num_positive_peaks.tsv
2025-11-24 14:23:54,342 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/spike_clusters.npy
2025-11-24 14:23:54,470 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/phy-export/exported/phy/block0_imec0.ap_recording1/cluster_si_unit_ids.tsv
2025-11-24 14:23:54,502 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/run_phy_20251124T184018UTC.log
2025-11-24 14:23:54,562 [INFO] Checking for remote processed data session directory /vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025:
logs
phy-export
sorted
2025-11-24 14:23:54,598 [INFO] Checking for processed data subdir logs:
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
2025-11-24 14:23:54,668 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/logs/phy-export_20251124T174934UTC_run_pipeline.log
2025-11-24 14:23:54,773 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/logs/aind-ephys-pipeline/nextflow-dag.html
2025-11-24 14:23:54,828 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/logs/aind-ephys-pipeline/nextflow-trace.txt
2025-11-24 14:23:54,886 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/logs/aind-ephys-pipeline/nextflow-timeline.html
2025-11-24 14:23:54,969 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/logs/aind-ephys-pipeline/nextflow-report.html
2025-11-24 14:23:55,142 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/logs/phy-export_20251124T175308UTC_process_detail.md
2025-11-24 14:23:55,230 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/logs/phy-export_20251124T174934UTC_nextflow.log
2025-11-24 14:23:55,309 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/logs/phy-export_20251124T175308UTC_nextflow.log
2025-11-24 14:23:55,362 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/logs/main_multi_backend_20251124T172227UTC_nextflow.log
2025-11-24 14:23:55,464 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/logs/main_multi_backend_20251124T172227UTC_run_pipeline.log
2025-11-24 14:23:55,524 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/logs/main_multi_backend_20251124T172227UTC_process_detail.md
2025-11-24 14:23:55,560 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/logs/phy-export_20251124T175308UTC_run_pipeline.log
2025-11-24 14:23:55,616 [INFO] Checking for processed data subdir sorted/nextflow:
find: ‘/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/sorted/nextflow’: No such file or directory
2025-11-24 14:23:55,662 [WARNING] Not downloading from subdir: sorted/nextflow
2025-11-24 14:23:55,662 [INFO] Checking for processed data subdir sorted/visualization:
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/sorted/visualization/block0_imec0.ap_recording1/traces_proc_seg0.png
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/sorted/visualization/block0_imec0.ap_recording1/motion.png
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/sorted/visualization/block0_imec0.ap_recording1/traces_full_seg0.png
/vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/sorted/visualization/block0_imec0.ap_recording1/drift_map.png
2025-11-24 14:23:55,717 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/sorted/visualization/block0_imec0.ap_recording1/traces_proc_seg0.png
2025-11-24 14:23:55,949 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/sorted/visualization/block0_imec0.ap_recording1/motion.png
2025-11-24 14:23:56,061 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/sorted/visualization/block0_imec0.ap_recording1/traces_full_seg0.png
2025-11-24 14:23:56,254 [INFO] Downloading to: /mnt/c/Users/labuser/Desktop/pipeline-results/BH/AS20-minimal3/03112025/sorted/visualization/block0_imec0.ap_recording1/drift_map.png
2025-11-24 14:23:56,353 [INFO] [chan 2] sftp session closed.
2025-11-24 14:23:56,354 [INFO] OK.