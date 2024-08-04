#!/bin/sh

echo
echo "        front end tests"
echo
node js/mod/presentMoment.test.js
echo
echo "        back end tests"
echo
python python/AfterSocketLogicTest.py
echo
echo "        system tests"
echo
sh scripts/test-sys.sh
