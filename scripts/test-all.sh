#!/bin/sh

f=git-ignores/test-result

echo
echo " ===  front end tests  ==="
echo
node js/mod/presentMoment.test.js
echo $? > $f-front
echo
echo " ===  back end tests  ==="
echo
python python/AfterSocketLogicTest.py
echo $? > $f-back
echo
echo " ===  system tests  ==="
echo
sh scripts/test-sys.sh
echo $? > $f-sys

test 0 = "$(head $f-front)" || exit 1
test 0 = "$(head $f-back)" || exit 1
test 0 = "$(head $f-sys)" || exit 1
