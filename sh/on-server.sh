#!/bin/sh

set -e

cd ..
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
. "../secrets.sh" || usage_and_exit
getopt_res="$(getopt -o tks -- "$@")" || usage_and_exit
eval set -- "$getopt_res"

while ! [ "x$1" = x-- ]; do
    case "$1" in
        -t)
            . "$secret_venv"/bin/activate
            python "$secret_uploaded"/run_unit_tests.py
            python "$secret_uploaded"/db_test.py
            ;;
        -k) secret_kill_old_with kill -s TERM ;;
        -s) secret_wrapper uvicorn main:app ;;
    esac
    shift
done
