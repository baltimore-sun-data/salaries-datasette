#! /bin/bash
set -eux -o pipefail

# Get the directory that this script file is in
THIS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

cd "$THIS_DIR"

venv-datasette/bin/datasette serve \
    --template-dir ./templates \
    --static static:./static \
    --metadata metadata.json \
    data/*.db
