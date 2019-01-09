# salaries-datasette
Public salary data acquired by the Baltimore Sun. Currently, we just have data from the state of Maryland for 2017.

## Usage

Run `./run.sh setup` to install locally. The script assumes you have either Python 3 or Homebrew for Mac installed. Run `./run.sh setup-frontend` to install front end dependencies.

Run `./run.sh create-db` to create a SQLite database out of the provided CSVs.

Run `./run.sh` or `./run.sh serve` to run server at http://localhost:9001.

Run the JS/CSS frontend server in another tab with `./run.sh frontend`.

`./run.sh format` will format Python and Javascript code according to the coding standards of the project.

`Dockerfile` is also provided for running/deploying with Docker. The image can be built with `./run.sh docker-build` and tested with `./run.sh docker`. The server only responds to correct hostnames (not localhost), so edit `/etc/hosts` to add `127.0.0.1   local.salaries.news.baltimoresun.com` and then test http://local.salaries.news.baltimoresun.com in the browser.
