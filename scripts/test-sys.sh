#!/bin/sh

(
    cd ./python
    . venv/bin/activate
    export KEYMOUTH_RAM_DB=yes
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
    then echo passed > git-ignores/systest-front-result.gitig
    else echo failed > git-ignores/systest-front-result.gitig
    fi
) &

wait

test passed = "$(head git-ignores/systest-front-result.gitig)" || exit 1
python python/systest_check.py || exit 2
