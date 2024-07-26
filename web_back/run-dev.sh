#!/bin/sh

set -e

echo_and_run() {
    printf ">"; printf " %s" "$@"; printf "\n"
    "$@"
    printf "done\n"
}

if ! [ -d venv ]
then echo_and_run python -m venv venv
fi
. venv/bin/activate

if ! command -v fastapi > /dev/null
then echo_and_run pip install fastapi
fi

echo_and_run fastapi dev main.py
