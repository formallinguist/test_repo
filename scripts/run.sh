#!/usr/bin/env bash

# run setup
source /nethome/rkchikkala/projects/htcondor-test/scripts/setup.sh

# run misc. stuff
nvidia-smi
echo $CUDA_VISIBLE_DEVICES
echo $HOSTNAME
which python
python -m pip list

# run code
python $PROJECT_DIR/src/htcondor_test/main.py
