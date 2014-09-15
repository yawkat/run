#!/bin/bash

dir=`dirname "$0"`

if [[ -f "$dir/pid" ]]; then
    if kill `cat "$dir/pid"`; then
        exit
    fi
fi

"$dir/main.py" $@ &
echo $! > "$dir/pid"
