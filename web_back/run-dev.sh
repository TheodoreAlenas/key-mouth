#!/bin/sh

set -e

if [ -d venv ]
then . venv/bin/activate
fi
if ! command -v fastapi > /dev/null
then pip install fastapi
fi

fastapi dev main.py
