#!/bin/bash

PYPY3=pypy3.9
LOG_DIR=`pwd`/microtest-logs/
PREV_LOG=$PYPYLOG

TESTS_DIR=$1
TESTS_DIR_DEFAULT="../tests/pyperformance/microtests/searching-results"

if [[ -v $1 || ! -d $1 ]]; then
    echo "[i] Using default tests path: $TESTS_DIR_DEFAULT"
    TESTS_DIR=$TESTS_DIR_DEFAULT
fi
echo "Start testing"

mkdir -p ${LOG_DIR}

$PYPY3 -m pip install -r $TESTS_DIR/requirements.txt &> /dev/null

pushd $TESTS_DIR > /dev/null
for TEST_DIR in */; do 
    pushd "$TEST_DIR" > /dev/null
    echo -e "\nAnalyzing ${TEST_DIR::-1}..." 
    for TEST in `find . -name "test-*.py"`; do
        echo -n "  Start test '${TEST:2:-3}'..."
        LOG_FILE="jit-backend-${TEST:7:-3}.dump"
        export PYPYLOG="jit-backend-dump:${LOG_FILE}"
        $PYPY3 $TEST &> /dev/null
        [[ $? == 0 ]] && echo "done." || echo "failed!"
        mv $LOG_FILE $LOG_DIR
    done
    popd > /dev/null
done
export PYPYLOG=${PREV_LOG}
popd > /dev/null
