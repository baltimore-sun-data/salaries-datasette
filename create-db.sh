#! /bin/bash
set -eux -o pipefail

echo "Clean data"
venv-datasette/bin/python scripts/clean_up.py

echo "Create DB file"
rm -rf data/cy2017-md.db
venv-datasette/bin/csvs-to-sqlite -t salary \
    -f first_name -f middle_initial -f last_name -f suffix -f organization -f subtitle \
    data/cy2017-md-updated.csv data/cy2017-md.db
