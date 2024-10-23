#!/bin/sh

set -e

usage="Usage: $0 ARGS

ARGS:
  -t  test DB and logic
  -k  kill the old instance
  -s  start Uvicorn

Examples:
  $0 -tks
  $0 -k
"

usage_and_exit() {
    printf "%s\n" "$usage" >& 2
    exit 1
}

if [ $# = 0 ]; then usage_and_exit; fi
. ./secrets.sh || usage_and_exit
export KEYMOUTH_DB="$secret_db"
getopt_res="$(getopt -o tks -- "$@")" || usage_and_exit
eval set -- "$getopt_res"

. "$secret_venv"/bin/activate

while ! [ "x$1" = x-- ]; do
    case "$1" in
        -t)
            python "$secret_uploaded"/python/run_unit_tests.py
            export KEYMOUTH_DB="$secret_db"
            python "$secret_uploaded"/python/db_test.py
            ;;
        -k) secret_kill_old_with kill -s TERM ;;
        -s) secret_wrapper uvicorn main:app ;;
    esac
    shift
done
