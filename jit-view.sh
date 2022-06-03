#!/bin/bash

PYPY2=pypy2.7
PYPY_DIR="$PWD/../pypy"
RPYTHON_DIR="${PYPY_DIR}/rpython"


if [[ -v $1 || ! -r $1 ]];then
    echo "No argument, set it please"
    exit
fi

strings=(${1//./ })
if [[ -v ${strings[1]} || ! ${strings[1]} == "dump" ]]; then
    echo "Not a .dump file"
fi

echo "viewer start working"
export PYTHONPATH=${PYPY_DIR}
${PYPY2} ${RPYTHON_DIR}/jit/backend/tool/viewcode.py $1