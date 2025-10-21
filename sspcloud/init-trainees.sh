#!/bin/bash

# Get the name of the repo
export MY_REPO=$(ls -d "/home/onyxia/work"/*/ | head -n 1 | xargs basename)

# Restore the environment
sh $MY_REPO/sspcloud/restore_environment.sh

# Download data
sh $MY_REPO/sspcloud/download_data.sh

# Download the notebook
# $1 is an argument giving the path of the notebook within the website (eg, notebooks/notebook1.ipynb)
export NOTEBOOK_PATH=$1
sh $MY_REPO/sspcloud/download_notebook.sh

# Ensure Quarto extension is up to date
code-server --install-extension quarto.quarto

# Additional configuration (system libs, etc.)
# sudo apt-get update
# sudo apt-get install ....
