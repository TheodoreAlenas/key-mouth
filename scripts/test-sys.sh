#!/bin/sh

set -e

(
    cd ./python
    . venv/bin/activate
    timeout 3s uvicorn                          \
            --host localhost                    \
            --port 8001                         \
            --log-config systest-log-config.ini \
            main:app
) &

sleep 1

(
    export KEYMOUTH_UI=the-ui-uri-isnt-used
    export KEYMOUTH_API=http://localhost:8001
    export KEYMOUTH_WS=ws://localhost:8001

    node js/mod/WebInteractor.systestMain.js
) &

wait

python python/systest-check.py
