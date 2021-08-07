#!/bin/sh

set -e

# Append repo dir to path
echo $PATH

export PATH=$PATH:/apps/nemde
export PYTHONPATH=/apps/nemde
echo $PATH

# Start worker
python3.9 /scripts/worker.py