#!/bin/bash

ENV_NAME="parlai_11.8"
CUDA_VER="11.8"

echo "STEP 0: set bash as the default shell for conda"
eval "$(command conda 'shell.bash' 'hook' 2> /dev/null)"

echo "Step 1: create the environment and activate it"
yes | conda create --prefix /home/jovyan/${ENV_NAME}
conda activate /home/jovyan/${ENV_NAME}

echo "Step 2: Install ipykernel and create kernel from the conda environment"
yes | conda install ipykernel
ipython kernel install --prefix /home/jovyan/${ENV_NAME} --name=${ENV_NAME}

echo "Step 3: follow the instructions from last command and copy the newly created kernel to /home/jovyan/.local/share/jupyter/kernels"
## example:
cp -r  /home/jovyan/${ENV_NAME}/share/jupyter/kernels/${ENV_NAME} /home/jovyan/.local/share/jupyter/kernels/

echo "STEP 4: install necessary packages"
yes | pip install parlai spacy transformers
yes | conda install pytorch cudatoolkit=${CUDA_VER} -c pytorch