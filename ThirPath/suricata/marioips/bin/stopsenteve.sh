#!/bin/sh
ps -aux | grep "senteve.sh" | awk '{print $2}' | sed -n '1'p | xargs kill -9
