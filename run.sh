#!/bin/sh

set -a
source .env
set +a

export PYTHONPATH="."
.venv/bin/python3 pitaco/application.py

