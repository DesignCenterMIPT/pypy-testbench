#!/bin/bash

PYPY3=pypy3.9
LOG_DIR=`pwd`/microtest-logs/
PREV_LOG=$PYPYLOG

if [ -v $1 ]; then
    echo "Please, set TEST_DIR env var"
    exit
else
    echo "Start testing"
fi


mkdir -p ${LOG_DIR}

$PYPY3 -m pip install -r $1/requirements.txt > /dev/null

pushd $1 > /dev/null
for TEST_DIR in */; do 
    pushd "$TEST_DIR" > /dev/null
    mkdir LOG_DIR
    echo -e "Analyzing ${TEST_DIR}..." 
    for TEST in `find . -name "test-*.py"`; do
        echo "Start test ${TEST:2:-3}..."
        LOG_FILE="jit-backend-${TEST:7:-3}.dump"
        export PYPYLOG="jit-backend-dump:${LOG_FILE}"
        $PYPY3 $TEST
        echo "Test Done"
        mv $LOG_FILE $LOG_DIR 
    done
    popd >> /dev/null
done
export PYPYLOG=${PREV_LOG}
popd >> /dev/null