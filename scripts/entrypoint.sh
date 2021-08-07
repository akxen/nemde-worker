#!/bin/sh

set -e

# Append repo dir to path
echo $PATH

export PATH=$PATH:/apps/nemde
export PYTHONPATH=/apps/nemde
echo $PATH

# Initialise casefile database
python3.9 /apps/nemde/scripts/initialise_tables.py
python3.9 /apps/nemde/scripts/upload_casefiles.py

# Start worker
python3.9 /scripts/worker.py