#!/bin/sh
iptables -F
ps -aux | grep "marioips.yaml -q" | awk '{print $2}' | sed -n '1'p | xargs kill -9
