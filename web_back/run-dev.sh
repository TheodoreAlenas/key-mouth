#!/bin/sh

set -e

if [ -d venv ]
then . venv/bin/activate
fi
if ! command -v fastapi > /dev/null
then pip install fastapi
fi

(cd .. && fastapi dev web_back_main.py)
