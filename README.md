# salaries-datasette
Public salary data acquired by the Baltimore Sun. Currently, we just have data from the state of Maryland for 2017.

## Usage

Run `setup.sh` to install locally. The script assumes you have either Python 3 or Homebrew for Mac installed.

Run `create-db.sh` to create a SQLite database out of the provided CSVs.

Run `serve.sh` to run server at http://localhost:8001.

`Dockerfile` is also provided for running/deploying with Docker.
