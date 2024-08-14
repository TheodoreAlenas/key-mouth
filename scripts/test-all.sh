#!/bin/sh

keep_res() {
    err=$?
    if ! [ 0 = $err ]
    then echo failed > git-ignores/test-result-"$1"
    else echo passed > git-ignores/test-result-"$1"
    fi
}
check() {
    test passed = "$(head git-ignores/test-result-"$1")" || exit 1
}
echo
echo "        front end tests"
echo
node js/mod/presentMoment.test.js
keep_res front
echo
echo "        back end tests"
echo
python python/AfterSocketLogicTest.py
keep_res back
echo
echo "        system tests"
echo
sh scripts/test-sys.sh
keep_res sys
check front
check back
check sys
