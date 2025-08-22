# Cortex User Setup

This doc should help you configure your cortex user account and local lab machine for running Geffen lab pipelines with Nextflow.

When you're done here please see [cortex-first-run.md](./cortex-first-run.md) to try processing some known data.

# WSL (on lab Windows machine)

If you're working from a Windows machine in the lab, it will be useful to set up [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) first.  "WSL" stands for "Windows Subsystem for Linux".  It's a Windows feature that provides a full Linux environment running within and alongside Windows.

Working from a Linux environment will have some advantages:
 - The local and cortex environments and command languages will be the same.
 - You'll be able run interactive programs like Phy with the processing and data on cortex, but the windows appearing on your local machine.

To install WSL find Windows Powershell in the task bar, open a Powershell window, and type:

```
wsl --install
```

This will take a few minutes then prompt you to reboot the machine.  After rebooting, open Powershell again and type:

```
wsl --install Ubuntu-24.04
```

This will make WSL use Ubuntu by default -- similar to cortex.  When prompted, set up a default Linux user for WSL.  Use the same credentials as the Windows machine.  Perhaps:

```
user: labuser
password: *******
```

Finally whenever you need to start WSL open a Powershell window and type:

```
wsl
```

From there you'll be working in Linux environment and you're ready to run all the commands below.

## Conda (WSL)

We can use [Conda](https://anaconda.org/anaconda/conda) to manage dependencies on the lab machine and on cortex.  To install conda on the local lab machine run the following:

```
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-py311_24.5.0-0-Linux-x86_64.sh -O miniconda.sh
chmod +x ./miniconda.sh 
./miniconda.sh 
# Follow the prompts.
# Choose "yes" to automatically initialize conda for shell.
```

To finish installing conda you'll need to log out from WSL and log in again.

```
# from WSL
exit

# from Powershell
wsl
```

Check that conda is installed in your WSL environment.

```
conda --version
# expect conda 24.5.0
```

## Conda environment (WSL)

With conda installed we can create our own conda environment for running lab Python scripts.  The environment is defined here in this repo in [geffen-pipelines.yml](./geffen-pipelines.yml).  To create and activate the environment in WSL:

```
cd ~
git clone https://github.com/benjamin-heasly/geffenlab-ephys-pipeline.git
conda env create -f geffenlab-ephys-pipeline/geffen-pipelines.yml
conda activate geffen-pipelines
```

Check that the environment is active and has the expected version of Python

```
python --version
# expect Python 3.13.5
```

# Connect to cortex

To connect to cortex from the WSL environment use `ssh -Y` like this:

```
ssh -Y ben@128.91.19.199
```

You would use your own username, rather than `ben`.

The `-Y` option enable interactive, graphical applications like Phy to run on cortex, but with the windows appearing on your local machine.

Once you've logged in to cortex you can test that graphics are working with a simple program like `xeyes`.  In your cortex terminal type:

```
xeyes
```

You should see a little window on your local machine, with two cartoon eyeballs that follow the mouse cursor.

# One-time cortex user setup

Before running your first pipeline you'll need to do some setup for your cortex user account.  This is to obtain pipeline code and install dependencies.

## Pipeline code

We're using two Nexftlow pipelines: the [AIND ephys pipeline](https://github.com/AllenNeuralDynamics/aind-ephys-pipeline) for spike sorting and quality metrics, and the [Geffen lab ephys pipeline](https://github.com/benjamin-heasly/geffenlab-ephys-pipeline) for combining data modalities and producing summary figures.

Clone these two Git repos into your cortex home folder:

```
mkdir ~/nextflow
cd ~/nextflow
git clone https://github.com/AllenNeuralDynamics/aind-ephys-pipeline.git
git clone https://github.com/benjamin-heasly/geffenlab-ephys-pipeline.git
```

## Conda (cortex)

We can use [Conda](https://anaconda.org/anaconda/conda) to manage dependencies on cortex as well as local lab machines.  To install conda for your cortex user run the following:

```
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-py311_24.5.0-0-Linux-x86_64.sh -O miniconda.sh
chmod +x ./miniconda.sh 
./miniconda.sh 
# Follow the prompts.
# Choose "yes" to automatically initialize conda for shell.
```

To finish installing conda you'll need to log out from cortex and log in again.

```
# from cortex
exit

# from local
ssh -Y ben@128.91.19.199
```

Check that conda is installed for your cortex user.

```
conda --version
# expect conda 24.5.0
```

## Conda environment (cortex)

With conda installed we can create our own conda environment for running Nextflow pipelines.  The environment is defined here in this repo in [geffen-pipelines.yml](./geffen-pipelines.yml).  It's the same one we used locally, above, for WSL.  To create and activate the environment on cortex:

```
cd ~/nextflow
conda env create -f geffenlab-ephys-pipeline/geffen-pipelines.yml
conda activate geffen-pipelines
```

Check that the environment is active and has the expected version of Java

```
java -version
# expect openjdk version "17.0.14" 2025-01-21 LTS
```

## Nextflow

Install the [Nextflow](https://www.nextflow.io/) pipeline tool for your cortex user.

```
cd ~/nextflow
wget https://github.com/nextflow-io/nextflow/releases/download/v25.04.6/nextflow-25.04.6-dist
chmod +x nextflow-25.04.6-dist
```

Check that nextflow is working:

```
./nextflow-25.04.6-dist -version

# expect
#      N E X T F L O W
#      version 24.10.6 build 5937
#      created 23-04-2025 16:53 UTC (12:53 EDT)
#      cite doi:10.1038/nbt.3820
#      http://nextflow.io
```

## Docker

Doker is already installed on cortex.  Check that your user is allowed to run Docker commands.

```
docker run hello-world
# expect
# Hello from Docker!
# This message shows that your installation appears to be working correctly.
```

# Screen

For long-running processes like our pipelines, you should use [screen](https://www.gnu.org/software/screen/) after connecting via `ssh`.  Screen allows your processing sessions to continue, even if you disconnect from `ssh` or if your network connection is interrupted.  This can save a lot of hassle if become disconnected during a long processing run.

Screen is already installed on cortex, here are some commands you can use.

## connect 

After connecting via `ssh`, start a screen session:

```
# start a screen session
screen
```

Then you can continue typing commands as normal.

## detach

When you want to detach:

```
screen -d   # detach from screen
```

If you need to detach while a long command is still running you can enable hot keys with `ctrl-a` then immediately press `d` (no need to press enter).

First press:

```
crtl-a      # enable hot keys
```

Then press:

```
d           # hotkey to detach from screen
```

This should bring you back to the terminal you saw right after you logged in with `ssh`.

## reattach

Later, when you want to reattach to your screen session, you can `ssh` to cortex and type:

```
screen -x   # reattach to existing screen session
```

This should bring you back to your running process, just as you left it.

## summary

Here's a summary of the command flow above.

```
                              screen              
                              or                  
┌────────┐  ssh   ┌────────┐  screen -x  ┌────────┐
│        ├───────►│        ├────────────►│        │
│ local  │        │ cortex │             │ screen │
│        │◄───────│        │◄────────────┤        │
└────────┘  exit  └────────┘  screen -d  └────────┘
                              or hotkeys          
                              ctrl-a, d           
```

## more

The commands above should get you started with screen.  Screen has many more capabilities, as in this [screen cheatsheet](https://gist.github.com/jctosta/af918e1618682638aa82).
