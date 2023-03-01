#!/bin/bash

# Create a new conda environment named "parlai_3.8" with Python 3.8
echo "STEP 1: create environment"
conda create -y -n parlai_3.8 python=3.8

# Activate the new environment
echo "STEP 2: activate conda with the shell"
eval "$(command conda 'shell.bash' 'hook' 2> /dev/null)"

echo "STEP 3: activate the new environment"
conda activate parlai_3.8

# Install packages using pip
echo "STEP 4: install dependencies"
pip install -q parlai transformers spacy fairseq

