# Run pipelines and sessions in batches.

This page gives an example of how to run multiple pipelines and sessions as a batch, all in one go.

We usually invoke pipelines using a Python script like [run_pipeline.py](../scripts/run_pipeline.py), one at a time, from the terminal command line.
Here we will invoke a batch of similar commands, one after another, from a separate Python script.

# Setup

First, let's get set up with a working Python environment.
This will be similar to how we run other [scripts](../scripts/), so you'll need to do one-time [cortex user setup](./cortex-user-setup.md) for your cortex user account.

From a terminal on Cortex, go to our [scripts](../scripts/) directory and activate our `geffen-pipelines` Conda environment.
Double check that you can find and run our existing scripts, like [run_pipeline.py](../scripts/run_pipeline.py).

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py --help
```

You should see help text like this:

```
usage: run_pipeline.py [-h] [--nextflow NEXTFLOW] [--config CONFIG] [--workflow WORKFLOW] [--report-template REPORT_TEMPLATE] [--work-dir WORK_DIR] [--raw-data-root RAW_DATA_ROOT]
                       [--processed-data-root PROCESSED_DATA_ROOT] [--analysis-root ANALYSIS_ROOT] [--experimenter EXPERIMENTER] [--subject SUBJECT] [--date DATE]

Run a Nextflow pipeline and aggregate logs to one place.

... etc ...
```

# Create a batch script

Next, let's create your batch script.
We'll start by having this print "Hello World", then build up to pipeline batch processing.

We can put batch scripts in the `scripts/` subdir of this repo.
This example will create `scripts/batch_demo.py`.
You should choose a different name for your own batch script: a name like `batch_ben.py` would make it clear that this is a batch script for the user `ben`.
Sticking to a convention like this should help avoid confusion.

You'll need a text editor to create your batch script.
[VSCode](https://code.visualstudio.com/) is a good option, which is already installed on Cortex.
You can create a script and launch VSCode using the `code` command.

```
code batch_demo.py
```

VSCode Popups:
 - VSCode might ask you to create a new keyring.  This is up to you.  Creating the keyring can help you configure VSCode extensions that automate tasks like logging into GitHub.
 - VSCode might ask you to install a Python extension.  This is also up to you.  Installing the extension will make editing your Python code easier and more pleasant.

In VSCode, add the following text to your batch script:

```
print("Hello World")
```

And save changes to the script.

# Run you script in the VSCode terminal

Open a new Terminal within VS code.
This will let you test your script as you make changes.
Go to:
 - `Terminal` -> `New Terminal`

Run the following in the VSCode terminal:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python batch_demo.py 
```

You should see your "Hello World" message printed in the terminal:

```
Hello World
```

# Import the `run_pipeline.py` script

"Hello World" is only a sanity check to test your environment, tools, etc.
Next we can start running pipeline scripts.

Edit your batch script to:
 - Delete the "Hello World" sanity check.
 - Import our existing [run_pipeline.py](../scripts/run_pipeline.py) script.
 - Print the `--help` text we saw earlier.

```
from run_pipeline import main

main(["--help"])
```

Run your script again and you should see the `--help` text for [run_pipeline.py](../scripts/run_pipeline.py).
Here's how it looks all together, in the VSCode terminal.

```
(geffen-pipelines) ben@cortex:/vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts$ python batch_demo.py 

usage: batch_demo.py [-h] [--nextflow NEXTFLOW] [--config CONFIG] [--workflow WORKFLOW] [--report-template REPORT_TEMPLATE] [--work-dir WORK_DIR] [--raw-data-root RAW_DATA_ROOT] [--processed-data-root PROCESSED_DATA_ROOT]
                     [--analysis-root ANALYSIS_ROOT] [--experimenter EXPERIMENTER] [--subject SUBJECT] [--date DATE]

Run a Nextflow pipeline and aggregate logs to one place.

... etc ...
```

`(geffen-pipelines)` confirms that we're using the correct Conda environment.

`/vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts` confirms that we're running from the correct directory.


# Run pipelines back-to-back

One you can call [run_pipeline.py](../scripts/run_pipeline.py) from your own Python script, you're free to code up some batch processing.
The arguments to the `main()` Python function are the same as the arguments we pass on the command line -- but now they can come from Python variables.

Here's an example script that reproduces the command line examples in [run-aind-ephys-pipeline.md](../docs/run-aind-ephys-pipeline.md) and [run-phy-export.md](../docs/run-phy-export.md).
The script calls the two pipelines back-to-back, so you don't have to wait for the AIND ephys pipeline to finish before issuing the next command.

To make the processing non-interactive, this script adds the `--ecephys-session-name` argument for [run_pipeline.py](../scripts/run_pipeline.py).

The script also passes in the `-resume` flag for Nextflow.
This should make it safe to re-run the entire batch, or restart after fixing an error.
Nextflow will verify which pipelines and sessions have already completed, and skip those instead of repeating them.

```
from run_pipeline import main

# Run the AIND ephys sorting pipeline on a minimal dataset, as in docs/run-aind-ephys-pipeline.md.
aind_ephys_args = [
  "--workflow", "geffenlab-ephys-pipeline/aind-ephys-pipeline/main_multi_backend.nf",
  "--config", "geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config",
  "--experimenter", "BH",
  "--subject", "AS20-minimal3",
  "--date", "03112025",
  "--input", "spikeglx",
  "--ecephys-session-name", "AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0",
  "-resume"
]
main(aind_ephys_args)

# Run the Geffen lab Phy export pipeline on the same dataset, as in docs/run-phy-export.md.
phy_export_args = [
  "--workflow", "geffenlab-ephys-pipeline/phy-export/phy-export.nf",
  "--config", "geffenlab-ephys-pipeline/phy-export/cortex.config",
  "--experimenter", "BH",
  "--subject", "AS20-minimal3",
  "--date", "03112025",
  "--input", "spikeglx",
  "--ecephys-session-name", "AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0",
  "-resume"
]
main(phy_export_args)
```

When you run this you should see lots of logging, similar to when you call [run_pipeline.py](../scripts/run_pipeline.py) from the terminal.
For example:

```
$ python batch_demo.py 

2026-03-03 10:49:25,865 [INFO] Writing logs for this script to stdout and /vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/main_multi_backend_20260303T154925UTC_run_pipeline.log
2026-03-03 10:49:25,865 [INFO] From work dir /vol/cortex/cd4/geffenlab/nextflow
2026-03-03 10:49:25,865 [INFO] Running workflow geffenlab-ephys-pipeline/aind-ephys-pipeline/main_multi_backend.nf

... etc ...

2026-03-03 10:49:41,474 [INFO] OK

2026-03-03 10:49:41,474 [INFO] Wrote the Nextflow log to /vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/phy-export_20260303T154933UTC_nextflow.log
2026-03-03 10:49:41,475 [INFO] Wrote details of each Nextflow processing step to /vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/phy-export_20260303T154933UTC_process_detail.md
2026-03-03 10:49:41,475 [INFO] Wrote a copy of this console log to /vol/cortex/cd4/geffenlab/processed_data/BH/AS20-minimal3/03112025/logs/phy-export_20260303T154933UTC_run_pipeline.log
```

# Run multiple sessions in a loop

The example above combines two pipelines back-to-back.
Finally, let's add a loop over multiple sessions.

This script adds a Python list to specify which sessions to run and a loop to iterate the list elements.

The script also uses a Python [try...except](https://docs.python.org/3/tutorial/errors.html#handling-exceptions) block to contain errors.
This way, a single-session error won't fail the entire batch.

```
from run_pipeline import main

# List all the sessions to process.
# Each session gets a tuple of (experimenter, subject, date, ecephys_session_name).
sessions = [
    ("BH", "AS20-minimal3", "03112025", "AS20_03112025_trainingSingle6Tone2024_Snk3.1_g0"),
    ("BH", "AS20-minimal3", "03112025", "another_session_test_g0"),
]

# Collect any exceptions so we can report them at the end.
exceptions = []

print(f"Starting batch of {len(sessions)} sessions:")
print(sessions)

for (experimenter, subject, date, ecephys_session_name) in sessions:

    print("\n")
    print(f"Starting session: {experimenter}, {subject}, {date}, {ecephys_session_name}")

    try:
        # Run the AIND ephys sorting pipeline, as in docs/run-aind-ephys-pipeline.md.
        aind_ephys_args = [
            "--workflow", "geffenlab-ephys-pipeline/aind-ephys-pipeline/main_multi_backend.nf",
            "--config", "geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config",
            "--experimenter", experimenter,
            "--subject", subject,
            "--date", date,
            "--input", "spikeglx",
            "--ecephys-session-name", ecephys_session_name,
            "-resume"
        ]
        main(aind_ephys_args)

        # Run the Geffen lab Phy export pipeline on the same dataset, as in docs/run-phy-export.md.
        phy_export_args = [
            "--workflow", "geffenlab-ephys-pipeline/phy-export/phy-export.nf",
            "--config", "geffenlab-ephys-pipeline/phy-export/cortex.config",
            "--experimenter", experimenter,
            "--subject", subject,
            "--date", date,
            "--input", "spikeglx",
            "--ecephys-session-name", ecephys_session_name,
            "-resume"
        ]
        main(phy_export_args)

    except Exception as exception:
        exceptions.append((experimenter, subject, date, ecephys_session_name, exception))
        print(f"Collected exception for {experimenter}, {subject}, {date}, {ecephys_session_name}:")
        print(exception)

print("\n")
print(f"Finished batch of {len(sessions)} sessions with {len(exceptions)} exceptions.")

for (experimenter, subject, date, ecephys_session_name, exception) in exceptions:
    print("\n")
    print(f"Had exception for {experimenter}, {subject}, {date}, {ecephys_session_name}:")
    print(exception)
```

# Custom batch scripts

The example batch script above is saved here in this repo as [batch_demo.py](../scripts/batch_demo.py).
You could copy this and write your own variation using different sessions, different pipeline arguments, etc.

To keep track of your work, remember how to run it later, etc., you can add your own script to this repo.
For example:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts

git add scripts/batch_demo.py
git commit -m "Add example script for batch processing multiple sessions."
git push
```
