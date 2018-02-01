set -eux -o pipefail

# Get the directory that this script file is in
THIS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

cd "$THIS_DIR"

echo "Test for Python 3"
[[ -z $(which python3) ]] && brew install python3

echo "Create Python virtual env"
python3 -m venv venv-datasette

echo "Pre-install setup Python"
venv-datasette/bin/pip install --upgrade pip setuptools wheel

echo "Install datasette"
venv-datasette/bin/pip install --no-deps --src src -r requirements.txt

echo "Clean data"
time venv-datasette/bin/python scripts/clean_up.py

echo "Create DB file"
rm -rf data/cy2017-md.db
time venv-datasette/bin/csvs-to-sqlite -t salary \
    -f first_name -f middle_initial -f last_name -f suffix -f organization -f subtitle \
    data/cy2017-md-updated.csv data/cy2017-md.db
