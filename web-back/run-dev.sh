#!/bin/sh

set -e

if [ -d venv ]
then . venv/bin/activate
fi

fastapi dev m.py
