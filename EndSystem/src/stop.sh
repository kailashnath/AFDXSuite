kill -9 `ps ax | grep 'python com/afdxsuite/afdx/__init__.py' | awk '(NR < 2){print $1}'`
