# Downstream Analysis

This doc should help you run downstream analysis, after running the [AIND ephys pipeline](./run-aind-ephys-pipeline.md) and the Geffen lab [Phy export pipeline](./run-phy-export.md).

A good first step is the [run_data_collection.py](https://github.com/jcollina/population-analysis/blob/main/run_data_collection.py) script from the lab's [population-analysis](https://github.com/jcollina/population-analysis) repo.  This combines raw behavior data in `.txt` and `.mat` files with spike sorting results.  It saves one or more pickles (Python `.pkl` files), containing dataframes of aligned data.  This script is intended to "just know" where raw and processed data are stored on cortex and to produce convenient, portable pickles for further analysis.  Read on for notes on how to run this.

From there you can load the pickles and do other analyses.

The [population-analysis](https://github.com/jcollina/population-analysis) repo has a Jyputer notebook [run_neuronal_multiplot.ipynb](https://github.com/jcollina/population-analysis/blob/main/run_neuronal_multiplot.ipynb) which uses the pickle data to generate a series of session summary plots.  Read on for notes on how to run this, too.

You can integrate these pickles as data sources into other custom analyses, see a simplified example below.

# Collect data with `run_data_collection.py`

Here's how to collect neuronal and behavioral data on cortex into one or more Python pickle files.

## get the `population-analysis` code

You can clone the [population-analysis](https://github.com/jcollina/population-analysis) repo (or your own analysis repo) into your home folder on cortex.
From a cortex terminal:

```
cd ~
git clone https://github.com/jcollina/population-analysis.git
```

## create a Python environment

Running analysis will require several Python dependencies.
We can manage these with Conda.
Create the `population-analysis` environment declared in [population-analysis.yml](https://github.com/jcollina/population-analysis/blob/main/population-analysis.yml).

```
cd ~/population-analysis
conda env create -f population-analysis.yml 
```

## collect data and save Python pickle(s)

[run_data_collection.py](https://github.com/jcollina/population-analysis/blob/main/run_data_collection.py) works like many of our other pipeline [scripts](../scripts/).  It locates data on cortex based on args like `--experimenter`, `--subject`, and `--date`.  See `python run_data_collection.py --help` for more details.

```
cd ~/population-analysis
conda activate population-analysis

python run_data_collection.py \
  --experimenter BH \
  --subject AS20-minimal3 \
  --date 03112025
```

This will search within the Geffen lab `/vol/cortex/cd4/geffenlab/raw_data/` directory for raw behavioral data (`.txt` and `.mat` files).

It will also search for trial events and spike sorting/curation results within `/vol/cortex/cd4/geffenlab/analysis/` (tprime event `.txt` and Phy `params.py` etc.).

For a given experimenter, subject, and date, the search might find data from multiple sessions or probes.  It will attempt to match up the behavioral and neuronal data for each session by sorting the search results on session name.

The result of this script should be one or more `neuronal_plus_behavioral.pkl` files, one for each session or probe.  Each pickle file will contain a dictionary of dataframes with aligned neuronal and behavioral data.

The pickles will be written within `/vol/cortex/cd4/geffenlab/analysis`:

![Ubuntu Files view of neuronal_plus_behavioral.pkl](./neuronal-plus-behavioral-pickle.png)

# Plot session summaries with `run_neuronal_multiplot.ipynb`

The notebook [run_neuronal_multiplot.ipynb](https://github.com/jcollina/population-analysis/blob/main/run_neuronal_multiplot.ipynb) can pick up where `run_data_collection.py` left off.  This notebook locates one of the saved pickles and generates a series of summary plots.

The notebook has several Python depenencies, including helper functions in the `population-analysis` repo itself.  The same `population-analysis` Conda environment used above should work here, too.

The notebook will save output figures in a subdirectory named `neuronal-multiplot`, in the same directory as the pickle.

![Ubuntu Files view of several neronal multiplot plots](./neuronal-multiplot-files.png)

Each of the multiplot plots should look something like this:

![Example of a population-analysis neuronal multiplot plot](./AS20-minimal3-03112025_neurons_1.png)

# Custom script starting from a saved pickle

You can integrate the pickles from `run_data_collection.py` into other analyses, much like the `run_neuronal_multiplot.ipynb` notebook does.
Here's a simplified example script that can find and load a pickle.

You could save the following code in a script like `my_analysis.py`:

```
from pathlib import Path
import pickle

import numpy as np

#
# Search for one or more .pkl files based on the standard data layout on cortex.
#
analysis_root = "/vol/cortex/cd4/geffenlab/analysis"
experimenter = "BH"
subject = "AS20-minimal3"
date = "03112025"
analysis_session_path = Path(analysis_root, experimenter, subject, date)

pickle_pattern = "neuronal-plus-behavioral/**/neuronal_plus_behavioral.pkl"
pickle_matches = list(analysis_session_path.glob(pickle_pattern))
if pickle_matches:
    pickle_path = pickle_matches[0]

#
# Or, specify a known pickle explicitly.
#
pickle_path = Path("/Users/benjaminheasly/Desktop/neuronal_plus_behavioral.pkl")

#
# Load the pickle into memory and select data of interest.
#
with open(pickle_path, 'rb') as pickle_in:
    df_dict = pickle.load(pickle_in)

pickle_subject = df_dict["subject"]
pickle_date = df_dict["date"]
print(f"Loaded pickle for subject {pickle_subject}, date {pickle_date}.")

#
# Summarize trial/behavior-related events.
#
trial_events = df_dict["trial_events"]
print(f"Loaded {len(trial_events)} trial events:")
print(trial_events)

#
# Summarize sorted spike events.
#
spikes_df = df_dict["spikes_df"]
clusters = spikes_df['cluster']
unique_clusters = np.unique(clusters)
cluster_count = len(unique_clusters)
print(f"Loaded {len(spikes_df)} spikes among {cluster_count} clusters:")
print(spikes_df)
```

This script has almost no dependenices, just Python 3.12 and NumPy.
You could run it like this:

```
python my_analysis.py
```

Or, you could cut and paste the same code into a Jupyter notebook.
When you run the code it will print a short summary of the pickled session data:

```
Loaded pickle for subject AS20-minimal3, date 03112025.

Loaded 14 trial events:

    stim_time  resp_time       stim  cat  acc  dir  resp
0    1.500161   2.136341  14.642410  3.0  1.0  1.0     1
1    6.119100   6.333228  12.550747  1.0  1.0  2.0     1
2   12.860785  13.110929  12.942934  1.0  1.0  2.0     1
3   18.514447  18.675405  14.773139  3.0  1.0  1.0     1
4   21.810618  22.045706  13.204392  1.0  1.0  2.0     1
5   25.352168  25.581004  14.642410  3.0  1.0  1.0     1
6   31.293812  31.495057  13.204392  1.0  1.0  2.0     1
7   34.899365  35.114998  12.550747  1.0  1.0  2.0     1
8   37.982192  38.112417  14.119494  3.0  1.0  1.0     1
9   42.462461  42.685646  12.681476  1.0  1.0  2.0     1
10  45.545286  46.729185  14.250223  3.0  0.0  2.0     1
11  52.105661  52.530091  14.250223  3.0  0.0  2.0     1
12  57.705954  57.958495  14.119494  3.0  1.0  1.0     1
13  62.399565  62.765754  14.511681  3.0  1.0  1.0     1

Loaded 102035 spikes among 164 clusters:

        cluster       time   ch interneuron_identity
0           126   0.000033   62                  NaN
1           155   0.000033  192                False
2           160   0.000033  375                  NaN
3           151   0.000033  260                  NaN
4           142   0.000033   52                  NaN
...         ...        ...  ...                  ...
102030      151  63.898245  260                  NaN
102031       57  63.898312    2                  NaN
102032       15  63.898412  220                 True
102033       15  63.898712  220                 True
102034       14  63.898879  220                  NaN

[102035 rows x 4 columns]
```
