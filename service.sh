#!/bin/bash

if pgrep "python" > /dev/null
then
    echo "Running"
else
    python /root/app.py
fi

