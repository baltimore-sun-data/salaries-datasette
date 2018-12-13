#!/bin/bash

set -eux -o pipefail

# Get the directory that this script file is in
THIS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

cd "$THIS_DIR"

ARGUMENT="${1:-serve}"

function serve() {
	local HOST="${1:-127.0.0.1}"
	local STATIC_DIR="${2:-./static}"

	venv-datasette/bin/datasette serve \
		--host "$HOST" \
		--port 9001 \
		--plugins-dir ./plugins \
		--template-dir ./templates \
		--static "static:$STATIC_DIR" \
		--metadata metadata.json \
		data/*.db
}

function setup() {
	local REQUIREMENTS="$1"
	local PYTHON="python3"

	# Travis breaks Python for some reason
	if [ -n "${TRAVIS:-}" ]; then
		PYTHON="/opt/python/3.6/bin/python"
	fi
	echo "Test for Python 3"
	[[ -z $(which "$PYTHON") ]] && brew install python3

	echo "Create Python virtual env"

	"$PYTHON" -m venv --clear venv-datasette

	echo "Pre-install setup Python"
	venv-datasette/bin/pip install --upgrade pip setuptools wheel

	echo "Install datasette"
	venv-datasette/bin/pip install --no-deps --src src -r "$REQUIREMENTS"
}

case "$ARGUMENT" in
serve)
	serve
	;;

serve-prod)
	export MANIFEST_FILE=dist/manifest.json
	serve 0 ./dist
	;;

frontend)
	cd frontend
	yarn run serve
	;;

setup)
	setup requirements-dev.txt
	;;

setup-prod)
	setup requirements.txt
	;;

setup-frontend)
	cd frontend
	node --version
	yarn --version
	yarn
	;;

create-db)
	venv-datasette/bin/python scripts/clean_up.py
	;;

format)
	venv-datasette/bin/black .
	venv-datasette/bin/flake8
	cd frontend
	yarn run lint
	;;

check-format)
	venv-datasette/bin/flake8
	venv-datasette/bin/black --check .
	cd frontend
	yarn run test
	;;

docker-build)
	docker-compose build
	;;

docker)
	docker-compose up
	;;

*)
	echo "Unknown argument: $ARGUMENT"
	echo "Known arguments are: serve setup create-db format check-format docker"
	exit 1
	;;
esac
