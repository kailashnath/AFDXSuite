#! /bin/sh

cd -P $(dirname $0)

APP_PATH=$PWD

export PYTHONPATH=$PYTHONPATH:$APP_PATH

python com/afdxsuite/afdx/__init__.py
