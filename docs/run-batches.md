# Run pipelines and sessions in batches.

This page gives an example of how to run multiple pipelines and sessions as a batch, all in one go.

We usually invoke each session and pipeline one at a time, from the command line, using a command line script like [run_pipeline.py](../scripts/run_pipeline.py).
We can invoke the same script many times in a row, using a loop and a wrapper Python script.

# Setup

First, let's get set up with a running Python environment.
This will be similar to how we run other [scripts](../scripts/), so you'll need to do one-time [cortex user setup](./cortex-user-setup.md) for your cortex user account.

From a terminal on Cortex, go to our [scripts](../scripts/) directory and activate our usual Conda environment.
Double check that you can find and run our existing scripts, like [run_pipeline.py](../scripts/run_pipeline.py).

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python run_pipeline.py --help
```

You should see help text printed, like this:

```
usage: run_pipeline.py [-h] [--nextflow NEXTFLOW] [--config CONFIG] [--workflow WORKFLOW] [--report-template REPORT_TEMPLATE] [--work-dir WORK_DIR] [--raw-data-root RAW_DATA_ROOT]
                       [--processed-data-root PROCESSED_DATA_ROOT] [--analysis-root ANALYSIS_ROOT] [--experimenter EXPERIMENTER] [--subject SUBJECT] [--date DATE]

Run a Nextflow pipeline and aggregate logs to one place.

... etc ...
```

# Create a wrapper script

Next, let's create your batch script/.
We'll start by printing "Hello World", then build from there to do pipeline batch processing. 

We can put batch scripts in the `scripts/` subdir of this repo.
This example will create `scripts/batch_demo.py`.
You should choose a different name for your own batch script: a name like `batch_ben.py` would make it clear that this is a batch script for the user `ben`, and this should help to avoid confusion.

You'll need a text editor to create your batch script.
[VSCode](https://code.visualstudio.com/) is a good option on Cortex.
You can create a script and launch VSCode with the `code` command.

```
code batch_demo.py
```

Popups:
 - VSCode might ask you to create a new keyring.  This is up to you.  Creating the keyring can help you configure VSCode extensions that do things like log in to GitHub, automatically.
 - VSCode might ask you to install a Python extension.  This is also up to you.  Installing the extension will make editing your Python code easier and more pleasant.

In VSCode, add the following text to your batch script:

```
print("Hello World")
```

And save changes to the script.

Open a new Terminal within VS code.
This will let you test your script as you make changes.
Go to:
 - `Terminal` -> `New Terminal`

Run the follwing in the VSCode terminal:

```
cd /vol/cortex/cd4/geffenlab/nextflow/geffenlab-ephys-pipeline/scripts
conda activate geffen-pipelines

python batch_demo.py 
```

You should see your "Hello World" message printed in the terminal:

```
Hello World
```

# Create a wrapper script

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

```
python batch_demo.py 
```
