#!/bin/sh

set -e

(
    cd ./python
    . venv/bin/activate
    export KEY_MOUTH_SHOW_WHO_TO=yes
    timeout 3s uvicorn                          \
            --host localhost                    \
            --port 8001                         \
            --log-config systest-log-config.ini \
            main:app
) &

sleep 1

(
    node js/mod/WebInteractor.systestMain.js \
         > git-ignores/systest-logs-front
) &

wait

python systest-check.py
