#!/bin/sh

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
    err=$?
    if [ 0 = $err ]
    then echo passed > git-ignores/systest-front-result
    else echo failed > git-ignores/systest-front-result
    fi
) &

wait

test passed = "$(head git-ignores/systest-front-result)" || exit 1
python python/systest-check.py || exit 2
