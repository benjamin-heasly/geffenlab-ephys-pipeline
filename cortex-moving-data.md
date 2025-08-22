# Cortex Moving Data

This doc should help you upload data from a local lab machine to cortex, and download pipeline results from cortex to a local lab machine.

Before running pipelines you'll need to do some one-time [cortex user setup](./cortex-user-setup.md) for your cortex user account and local lab machine.

# Upload data from local lab machine to cortex

This repo has a Python script [upload_data.py](./data/upload_data.py) that should help uploading data from your local lab machine to cortex.  Internally this uses `ssh` to connect to cortex, but the Python wrapper should make it more convenient.


# Download results cortex to local lab machine