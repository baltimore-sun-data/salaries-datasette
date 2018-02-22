#! /bin/bash
set -eux -o pipefail

venv-datasette/bin/python scripts/clean_up.py
